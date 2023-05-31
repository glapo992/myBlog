# gneral imports
from app import db
from datetime import datetime 

# login stuff
from flask_login import UserMixin # generic login implementations suitable for most user model classes
from app import login

# pw hashing-> already provided in flask
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5 # optional, just for Gravatar service for avatar images

""" after a modificaion in the models, the migrate class will generate a script with the database version. 
run commands in the terminal:
flask db migrate -m <optional comments> --> creates the script that update the db with modifications on models (sort of git)
flask db upgrade --> applies the script to the database
flask db downgrade --> retunrs to a previous version of the db 

to add a record in the terminal:
python3
>>> from app import app, db
>>> from app.models import User, Posts
>>> app.app_context().push()      # allows sqlalchemy to acceed the ap.config without give app as argument
>>> u = Users(username='jj', email='jj@bravo.it')
>>> db.session.add(u)
>>> db.session.commit()  # write the data in the database

"""

class Users(UserMixin ,db.Model): # added UserMixin at the user class
    """ some of the user already created for testing:
    username:pw
    - Giovanni:il_paradiso
    - Aldo:della
    - Giacomino:brugola
    - dr:pw
    """
    id       = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email    = db.Column(db.String(64), index = True, unique = True)
    pw_hash  = db.Column(db.String(128))
    posts    = db.relationship('Posts', backref = 'author', lazy = 'dynamic') # reference to the post Model class(not table name!!), is not a db field but a view of the realtionship
    about_me = db.Column(db.String(150))
    last_seen= db.Column(db.DateTime, default = datetime.utcnow)

    # hashing password--------------
    def set_password(self, password:str)->str:
        """generates a hash for the given pw and set it as param of the class

        :param password: hash
        :type password: str
        """
        self.pw_hash = generate_password_hash(password=password)

    def check_password(self, password:str)->bool:
        """check if the given password's hash is the same of the saved one

        :param password: passwd to check
        :type password: str
        :return: result of check
        :rtype: bool
        """
        return check_password_hash(self.pw_hash, password=password)
    #-------------------------------
   
    def avatar(self, size:int)->str:
        """generate an avatar image form the md5 hash of the email and return a link to insert in the img tag in html

        :param size: the dimension in px of the image(128, 64, 32 etc)
        :type size: int
        :return: link to the source
        :rtype: str
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()  # obtain the digest of the md5 hash of the email
        return 'https://www.gravatar.com/avatar/{}?d=robohash&s={}&r=r'.format(digest, size)    # just the link of the service. can be added an r parameter fro the rating of the image (acc values are: g, pg, r, x)
    
    def __repr__(self):
        return'<User {}>'.format(self.username)
    
class Posts(db.Model):
    id        = db.Column(db.Integer, primary_key = True)
    body      = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index = True, default=datetime.utcnow)  # utcnow is a function and is passed completely (without "()"), not the return value, so the timestamp is converted to the user's machine time
    user_id   = db.Column(db.Integer, db.ForeignKey('users.id')) # how to set a foregin key. the user table is used, not the class User above

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    

@login.user_loader
def load_user(id):
    return Users.query.get(int(id)) # querys the users id and convert into a int (only if is so saved in the databse's column)