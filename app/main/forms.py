from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import Users
from flask_babel import lazy_gettext as _l

class LoginForm(FlaskForm):
    username    = StringField  (_l('Username'), validators=[DataRequired(),Length(min=0, max=64)])
    password    = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField (_l('Remember me'))
    submit      = SubmitField  (_l('sign in'))

class RegistrationForm(FlaskForm):
    username  = StringField  (_l('Username'),         validators=[DataRequired(), Length(min=0, max=64)])
    email     = EmailField   (_l('email'),            validators=[DataRequired(), Email(), Length(min=0, max=64)])
    password  = PasswordField(_l('Password'),         validators=[DataRequired()])
    password2 = PasswordField(_l('Confirm Password'), validators=[DataRequired(), EqualTo('password')])
    submit    = SubmitField  (_l('Register now'))

# custom validators named "validate_<name_field>" are automaticcaly called by WTForms ad validators in the respective field
    def validate_username(self, username):
        """ search for another user with the same username in the db """
        user = Users.query.filter_by(username= username.data).first()
        if user is not None:
            raise ValidationError(_l('username already exixts'))  # message flashed in case the validation fail
        
    def validate_email(self, email):
        """ search for another user with the same email in the db """
        user = Users.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError(_l('email already used'))
        
class EditProfileForm(FlaskForm):
    """form allows user to edit his personal profile info"""
    
    username  = StringField  (_l('Username'), validators=[DataRequired()]) 
    about_me  = TextAreaField(_l('About me'), validators=[Length(min=0, max=150)])
    submit    = SubmitField  (_l('Edit'))

    def __init__(self, original_username, *args, **kwargs): # the original_username must be passed from the view function 
        super (EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username  # creates a new var with the orignal name of the user

    def validate_username(self, username):
        """custom validator, check if the username chosen is already in use and raises an error

        :param username: new chosen username
        :type username: str
        :raises ValidationError: error
        """
        if username.data != self.original_username:
            user = Users.query.filter_by(username = self.username.data).first()   # search in the db if there are other users with the same username
            if user is not None:
                raise ValidationError(_l('Please choose another user'))  # if there are other users with the chosen username, raise an error

class EmptyForm(FlaskForm):
    """allows to generate a form with only a button, so you can integrate it as a POST request and send data without make them appear in the url like a GET"""
    submit = SubmitField(_l('Submit'))

class PostForm(FlaskForm):
    """Form allows to add posts"""
    post   = TextAreaField(_l('say something'), validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))

class ResetPasswordRequestForm(FlaskForm):
     """form that send a reset password request -> wll be sent via email """
     email  = EmailField(_l('email'), validators=[DataRequired(), Email(), Length(min=0, max=64)])
     submit = SubmitField(_l('Request Password restet'))

class ResetPasswordForm(FlaskForm):
    """form to actually reset the password"""
    password  = PasswordField(_l('New Password'),     validators=[DataRequired()])
    password2 = PasswordField(_l('Confirm Password'), validators=[DataRequired(), EqualTo('password')])
    submit    = SubmitField  (_l('change password'))