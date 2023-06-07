import os
basedir = os.path.abspath(os.path.dirname(__file__)) # var with the abs path of this file

class Config(object):
    """defines configuration settings for the app, if new configuration are needed they can be added to this class.
    vars are read from .falskenv (remember to install flask-dotenv to read this file)
    """
    #! REMOVE THE .flaskenv FILE FROM GIT BEFORE DEPLOY AND SET A REAL SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_password' # var used as key for cryptogtaphy and tokens, used by wtf 
    
    # tryes to reate a connection with postgres db reading from configs, if cant, uses the local db
    # TODO: remove the local db in prod 
    try:
        PASSWORD = os.environ.get('DB_PASSWORD') 
        USERNAME = os.environ.get('DB_USERNAME') 
        HOST     = os.environ.get('DB_HOST') 
        DB_NAME  = os.environ.get('DB_DB_NAME') 

        if USERNAME and PASSWORD and HOST and DB_NAME:
            db_url = "postgresql://{}:{}@{}/{}".format(USERNAME,PASSWORD,HOST,DB_NAME)
        else:
            raise KeyError('Some necessary environment variable(s) are not defined')
        SQLALCHEMY_DATABASE_URI = db_url
    except:  
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


    # Pagination configs
    POST_PER_PAGE = 5 # definition of how many post per page is possible to see
    POST_PER_PAGE_EXPLORE = 10 # definition of how many post per page is possible to see