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

#------NOT A VIEW-----------
# the decorated function is executed right before ANY view function in the application.
@app.before_request 
def before_request():
    """records the timedate of the visit of a user and saves it in the db"""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
#---------------------



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = "home")


# -----------------------AUTENTICATION VIEWS----------------------------
@app.route('/login', methods=['GET', 'POST']) # this method accepts also post requests, as specified in the html from 
def login():
    """ the login library has required items that can be used 
    - is_authenticated: a property that is True if the user has valid credentials or False otherwise.
    - is_active: a property that is True if the user's account is active or False otherwise.
    - is_anonymous: a property that is False for regular users, and True for a special, anonymous user.
    - get_id(): a method that returns a unique identifier for the user as a string (unicode, if using Python
    """
    if current_user.is_authenticated:
        return redirect (url_for('index'))                      #  if the user is already auth, just return the index
     
    form = LoginForm()
    if form.validate_on_submit():                               # procss the form, returns true or false depending on the validators. if false require an error handler
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('invalid username or pw')                     # must be handled in html. did in base.html so all pages can handle flash messages
            return redirect(url_for('login'))                   # redirect with the url_for method
        login_user(user=user, remember=form.remember_me.data)   #flask function register the user as logged in. sets a variable current_user with the logged one for the duration of the session
        next_page = request.args.get('next')                    # the argument of the request -> is the url to the page the user want to visit, caught by @login_required (.../login?next=%2Fproject)
        
        if not next_page or url_parse(next_page).netloc != "":  
            # ensure that the next is on the same site 
            #(an attacker could insert a different url in the ?next and have the login token to acceed also if is on another site). 
            #to determne if the url is relative or not, the netloc comonent must exixt
            next_page = (url_for('index'))  # if next page does not exist, the url for index is assigned
        return redirect (next_page)

    return render_template ('login.html', form = form, title = 'Sign In')

@app.route('/logout')
def logout():
    """logs out the already logged user """
    logout_user()
    return redirect(url_for('index'))

@app.route('/registration', methods=['GET', 'POST']) # this method accepts also post requests, as specified in the html from 
def registration():
    if current_user.is_authenticated:
        return redirect (url_for('index'))    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('registration ok')
        return redirect(url_for('login'))
    return render_template('registration.html', form = form , title= 'Registration')   

#----------------------------------------------------------------------------------------

#------------USER PAGE--------------------------------------------------------------
@app.route('/user/<username>')
@login_required    # view is protected by non-logged users
def user (username):
    user = Users.query.filter_by(username = username).first_or_404() # this method returns a 404 error if user is null
    
    posts = Posts.query.filter_by(user_id = user.id)
    form = EmptyForm()  # manage the follow/unfollow feature, must be passed as argument in the retun
    form_del = EmptyForm()  # other form for delete posts


    return render_template('user.html', user=user, posts=posts, form_del=form_del, title = user.username, form = form)


@app.route('/user/<username>/edit_profile', methods=['GET', 'POST']) # this method accepts also post requests, as specified in the html from 
@login_required  # view is protected by non-logged users
def edit_profile(username):
    """page to edit the profile info of the user, accessed only from the user's page after a login"""
    form = EditProfileForm(current_user.username)   # current_user.username is passed to the function of control purposes
    if form.is_submitted():
        print ("submitted")
    if form.validate():
        print ("valid")
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('changes saved')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':       # if the form is asked for the first time (GET), is pre-populated with database info. it wont happend if there is a validation error(POST)
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form = form, title = 'edit profile - {}'.format(current_user.username))

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    """this function does't have a view but performs an action and returns another view"""
    form = EmptyForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username = username).first()  #search on database the user with the given username
        # managing of wrong cases
        if user is None:
            flash('user {} not found'.format(username))
            return redirect (url_for('index'))
        if user == current_user:
            flash ('no autoerothism please')
            return redirect(url_for('user', username=username))
        # calls of the follow function
        current_user.follow(user)
        db.session.commit()
        flash ('now you follow {}'.format(username))
        return redirect (url_for('user', username=username))
    else :
        return redirect (url_for('index'))
    


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    """this function does't have a view but performs an action and returns another view"""
    # same as follow, but unfollow() is used here
    form = EmptyForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username = username).first()
        if user is None:
            flash('user {} not found'.format(username))
            return redirect (url_for('index'))
        if user == current_user:
            flash ('no autoerothism please')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash ('now you don\' follow {} anymore'.format(username))
        return redirect (url_for('user', username=username))
    else :
        return redirect (url_for('index'))

# this is another methot to add a routing rule to a function, is the same than the decorator
#app.add_url_rule('/edit_profile', 'edit_profile', edit_profile,  methods=['GET', 'POST'])

#----------------------------------------------------------------------------------------

@app.route('/project',methods = ['GET', 'POST'])
@login_required   # view is protected by non-logged users
def project():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(body= form.post.data, author = current_user)  
        db.session.add(post)
        db.session.commit()
        flash('posted!')
        form.post.data = ""

    posts = current_user.followed_posts().all()   # function that shows all post from followed people and from user
    form_del = EmptyForm()  # other form for delete posts
    return render_template('project.html', form = form, form_del =  form_del,title = "proj", posts = posts)


@app.route('/')
@app.route('/explore')
@login_required
def explore():
    posts = Posts.query.order_by(Posts.timestamp.desc()).all()
    # return the template of proj page because is very similar, but without the form to insert posts. 
    # must add a condition in the template to prevent a crash
    return render_template('project.html', title = "home", posts = posts)



@app.route('/delete_post/<del_post_id>' ,methods=['POST'])
@login_required
def delete_post(del_post_id):
    """ function to delete a record from the database"""
    form = EmptyForm()
    if form.validate_on_submit():
        del_post = Posts.query.filter_by(id = del_post_id).first()
        db.session.delete(del_post)
        db.session.commit()
        flash('post deleted succesfully')
    return redirect (url_for('project'))