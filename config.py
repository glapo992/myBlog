import os
basedir = os.path.abspath(os.path.dirname(__file__)) # var with the abs path of this file

class Config(object):
    """defines configuration settings for the app, if new configuration are needed they can be added to this class
    vars are read from .falskenv (remember to install flask-dotenv to read this file)
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_password' # var used as key for cryptogtaphy and tokens, used by wtf 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+ os.path.join(basedir, 'app.db') # reading config. if no path to db, it creates one in the basedir
    SQLALCHEMY_TRACK_MODIFICATIONS = False