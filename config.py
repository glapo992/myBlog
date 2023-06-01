import os
basedir = os.path.abspath(os.path.dirname(__file__)) # var with the abs path of this file

class Config(object):
    """defines configuration settings for the app, if new configuration are needed they can be added to this class.
    vars are read from .falskenv (remember to install flask-dotenv to read this file)
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_password' # var used as key for cryptogtaphy and tokens, used by wtf 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+ os.path.join(basedir, 'app.db') # reading config. if no path to db, it creates one in the basedir
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # next 2 vars activates the development mode, which allows to access to a debugger from the brewser and auto reload the server when a chage in a file is detected, never use in production
    FLASK_ENV=os.environ.get('FLASK_ENV')   # can be development or production
    FLASK_DEBUG=os.environ.get('FLASK_DEBUG') # this is a bool, only accepts 1 or 0

    # email configuration for error report
    # when an error aoocurs, an email is sent to the specified addr.
    # for the moment is not fully configured, but values can be added to the .flaskenv file
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']  # list of reciving addresses