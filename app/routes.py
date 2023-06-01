from app import app, db # from app module import app obj (is a Flask obj)
from flask import render_template, flash, redirect, url_for, request
from datetime import datetime


# login/registration imports
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import Users
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


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
    
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    
    return render_template('user.html', user=user, posts=posts, title = user.username)


@app.route('/user/current_user.username/edit_profile', methods=['GET', 'POST']) # this method accepts also post requests, as specified in the html from 
@login_required  # view is protected by non-logged users
def edit_profile():
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
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':       # if the form is asked for the first time (GET), is pre-populated with database info. it wont happend if there is a validation error(POST)
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    # print('validation: ', (repr(form.validate_on_submit())))
    # print('errors: ', form.errors)
    # print('token: '+ str(form.csrf_token))
    return render_template('edit_profile.html', form = form, title = 'edit profile')

#----------------------------------------------------------------------------------------

@app.route('/project')
@login_required   # view is protected by non-logged users
def project():
    posts =  [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('project.html', title = "proj", posts = posts)
