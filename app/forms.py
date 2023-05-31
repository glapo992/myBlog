from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import Users

class LoginForm(FlaskForm):
    username    = StringField  ('Username', validators=[DataRequired()])
    password    = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField ('Remember me')
    submit      = SubmitField  ('sign in')

class RegistrationForm(FlaskForm):

    username  = StringField  ('Username', validators=[DataRequired()])
    email     = EmailField   ('email', validators=[DataRequired(), Email()])
    password  = PasswordField('Password', validators=[DataRequired()])
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
    username = StringField('Username', validators=[DataRequired()]) 
    about_me = TextAreaField('About me', validators=[Length(min=0, max=150)])
    submit   = SubmitField('Submit')