from app import app, db # from app module import app obj (is a Flask obj)
from flask import Response, render_template, flash, redirect, url_for, request
from datetime import datetime


# login/registration imports
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import Users
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

# follow/unfollow
from app.forms import EmptyForm

# form insertion
from app.forms import PostForm
from app.models import Posts

# password reset via mail 
from app.forms import ResetPasswordRequestForm, ResetPasswordForm 
from app.email import send_password_reset_email

#language support
# import the function _() that acts like a wrapper arpund the text to translate, lazy_gettext() does the same but waits an http request before transalte the text
from flask_babel import _, get_locale
from flask import g 
# lang detection ajax
from langdetect import detect, LangDetectException
from flask import jsonify
from app.translate import translate



#------NOT A VIEW-----------
# the decorated function is executed right before ANY view function in the application.
@app.before_request 
def before_request():
    #records the timedate of the visit of a user and saves it in the db
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    # conversion of locale() to str so it is translatable
    g.locale= str(get_locale())
#---------------------

#------TRANSLATION SERVICE-----------
@app.route('/translate', methods=['POST'])
@login_required
def translate_text():
    # invocatoion of the transalte function with datas from the request 
    return jsonify({'text':translate(
                                        request.form['text'],
                                        request.form['source_language'],
                                        request.form['dest_language'])})





@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = "home")



#------------USER PAGE--------------------------------------------------------------
@app.route('/user/<username>')
@login_required    # view is protected by non-logged users
def user (username):
    """user main page, where all his post are shown

    :param username: the username of the user
    :type username: str
    """
    user = Users.query.filter_by(username = username).first_or_404() # this method returns a 404 error if user is null
    
    page = request.args.get('page', 1, type=int)
    #posts = Posts.query.filter_by(user_id = user.id).order_by(Posts.timestamp.desc())
    posts = user.posts.order_by(Posts.timestamp.desc()).paginate(page = page, per_page = app.config['POST_PER_PAGE'], error_out = False) # shows some posts per page ( see pagination )
    next_url = url_for('user', username=user.username, page = posts.next_num) if posts.has_next else None # next_num is a Paginate() atribute
    prev_url = url_for('user', username=user.username, page = posts.prev_num) if posts.has_prev else None # prev_num is a Paginate() atribute

    form = EmptyForm()  # manage the follow/unfollow feature, must be passed as argument in the retun
    form_del = EmptyForm()  # other form for delete posts


    return render_template('user.html', user=user, posts=posts, form_del=form_del, title = user.username, form = form, next_url = next_url, prev_url= prev_url)


@app.route('/user/<username>/edit_profile', methods=['GET', 'POST']) # this method accepts also post requests, as specified in the html from 
@login_required  # view is protected by non-logged users
def edit_profile(username):
    """page to edit the profile info of the user, accessed only from the user's page after a login"""
    
    form = EditProfileForm(current_user.username)   # current_user.username is passed to the function for control purposes
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('changes saved'))
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':       # if the form is asked for the first time (GET), is pre-populated with database info. it wont happend if there is a validation error(POST)
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form = form, title = _('edit profile - {}'.format(current_user.username)))

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    """this function does't have a view but performs an action and returns another view"""
    form = EmptyForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username = username).first()  #search on database the user with the given username
        # managing of wrong cases
        if user is None:
            flash(_('user {} not found'.format(username)))
            return redirect (url_for('index'))
        if user == current_user:
            flash (_('no autoerothism please'))
            return redirect(url_for('user', username=username))
        # calls of the follow function
        current_user.follow(user)
        db.session.commit()
        flash (_('now you follow {}'.format(username)))
        return redirect (url_for('user', username=username))
    else :
        return redirect (url_for('index'))
    


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    """this function doesnt tertun a template, performs an action and returns another view"""
    # same as follow, but unfollow() is used here
    form = EmptyForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username = username).first()
        if user is None:
            flash(_('user {} not found'.format(username)))
            return redirect (url_for('index'))
        if user == current_user:
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash (_('now you don\' follow {} anymore'.format(username)))
        return redirect (url_for('user', username=username))
    else :
        return redirect (url_for('index'))

# this is another methot to add a routing rule to a function, is the same than the decorator:
#app.add_url_rule('/edit_profile', 'edit_profile', edit_profile,  methods=['GET', 'POST'])

#----------------------------------------------------------------------------------------

@app.route('/feed',methods = ['GET', 'POST'])
@login_required   # view is protected by non-logged users
def feed():
    """view that shows only posts from user and followed profiles and allows the user to write new posts"""
    form = PostForm()
    if form.validate_on_submit():
        # add language detection with ajax
        try:
            language = detect(text=form.post.data)
        except LangDetectException:
            language = ""
        
        post = Posts(body= form.post.data, author = current_user, language = language)  
        db.session.add(post)
        db.session.commit()
        flash(_('posted!'))
        form.post.data = ""
    # pagination handling
    page = request.args.get('page', 1, type=int)
    #posts = current_user.followed_posts().all()   # function that shows all post from followed people and from user
    posts = current_user.followed_posts().paginate(page = page, per_page = app.config['POST_PER_PAGE'], error_out = False) # shows some posts per page ( see pagination )
    # creation of url to send to the template to naviagate the pagination
    next_url = url_for('feed', page = posts.next_num) if posts.has_next else None # next_num is a Paginate() atribute
    prev_url = url_for('feed', page = posts.prev_num) if posts.has_prev else None # prev_num is a Paginate() atribute
    
    form_del = EmptyForm()  # other form for delete posts
    return render_template('feed.html', form = form, form_del = form_del, title = "Feed", posts = posts, next_url = next_url, prev_url= prev_url)


@app.route('/')
@app.route('/explore')
@login_required
def explore():
    """view shows all posts from all users """
    # pagination handling
    page = request.args.get('page', 1, type=int)

    # posts = Posts.query.order_by(Posts.timestamp.desc()).all() # returns all results
    posts = Posts.query.order_by(Posts.timestamp.desc()).paginate(page = page, per_page = app.config['POST_PER_PAGE_EXPLORE'], error_out = False)

    # creation of url to send to the template to naviagate the pagination
    next_url = url_for('explore', page = posts.next_num) if posts.has_next else None # next_num is a Paginate() atribute
    prev_url = url_for('explore', page = posts.prev_num) if posts.has_prev else None # prev_num is a Paginate() atribute
    # return the template of proj page because is very similar, but without the form to insert posts. 
    # must add a condition in the template to prevent a crash
    return render_template('feed.html', title = _("Explore"), posts = posts, next_url = next_url, prev_url= prev_url)



@app.route('/delete_post/<del_post_id>' ,methods=['POST'])
@login_required
def delete_post(del_post_id):
    """ function to delete a post from the database"""
    form = EmptyForm()
    if form.validate_on_submit():
        del_post = Posts.query.filter_by(id = del_post_id).first()
        db.session.delete(del_post)
        db.session.commit()
        flash(_('post deleted succesfully'))
    return redirect (url_for('feed'))