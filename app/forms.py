from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import Users

class LoginForm(FlaskForm):
    username    = StringField  ('Username', validators=[DataRequired(),Length(min=0, max=64)])
    password    = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField ('Remember me')
    submit      = SubmitField  ('sign in')

class RegistrationForm(FlaskForm):

    username  = StringField  ('Username',         validators=[DataRequired(), Length(min=0, max=64)])
    email     = EmailField   ('email',            validators=[DataRequired(), Email(), Length(min=0, max=64)])
    password  = PasswordField('Password',         validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit    = SubmitField  ('Register now')

# custom validators named "validate_<name_field>" are automaticcaly called by WTForms ad validators in the respective field
    def validate_username(self, username):
        """ search for another user with the same username in the db """
        user = Users.query.filter_by(username= username.data).first()
        if user is not None:
            raise ValidationError('username already exixts')  # message flashed in case the validation fail
        
    def validate_email(self, email):
        """ search for another user with the same email in the db """
        user = Users.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('email already used')
        
class EditProfileForm(FlaskForm):
    """from alows user to edit his personal profile info"""
    
    username  = StringField  ('Username', validators=[DataRequired(),Length(min=0, max=64)]) 
    about_me  = TextAreaField('About me', validators=[Length(min=0, max=150)])
    submit    = SubmitField  ('Edit')

    def __init__(self, original_username, *args, **kwargs): # the original_username must be passed from the view function 
        super (EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username  # creates a new var with the orignal name of the user

    def validate_username(self, username):
        """custom validator, chechk if the username chosen is already in use and raises an error

        :param username: new chosen username
        :type username: str
        :raises ValidationError: error
        """
        if username.data != self.original_username:
            user = Users.query.filter_by(username = self.username.data).first()   # search in the db if there are other users with the same username
            if user is not None:
                raise ValidationError('Please choose another user')  # if there are other users with the chosen username, raise an error

class EmptyForm(FlaskForm):
    """allows to generate a form with only a button, so you can integrate it as a POST request and send data without make them appear in the url like a GET"""
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    """Form allows to add posts"""
    post = TextAreaField('say something', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')


class ResetPasswordRequestForm(FlaskForm):
     """form for reset password """
     email = EmailField('email', validators=[DataRequired(), Email(), Length(min=0, max=64)])
     submit = SubmitField('Request Password restet')