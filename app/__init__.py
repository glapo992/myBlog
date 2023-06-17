""" in this module are initialyzed all the objects that are used in the whole /app folder"""
from flask import Flask
from config import Config # environmental config

from flask_sqlalchemy import SQLAlchemy # database stuff
from flask_migrate import Migrate
import psycopg2 # just for future db connection with postgres

from flask_login import LoginManager # Login

#log erors
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

#email support
from flask_mail import Mail

#bootstrap
from flask_bootstrap import Bootstrap
 

#FLASK SETTINGS---------------------
try:
    app = Flask(__name__)
    app.config.from_object(Config) # import configs from the Class Config in the as-named module. the values are accessed with a dict-like statement (app.config['SECRET_KEY'])
except:
    raise Exception('impossible to read the configuration')
#-----------------------------------

#BOOTSTRAP------------------------------
#init of bootsrap object, creates a new html base page called bootstrap/base.html, the actual base.html must be adapted to extend bootstrap version
bootstrap = Bootstrap(app=app) 



# DATABASE--------------------------
# to initialize a new db run on the terminal 'flask db upgrade':it will execute the script auto generated by the migration engine
try:
    db = SQLAlchemy(app)    # creation of the database obj
    migrate = Migrate(app, db) # the migration engine, creates a repo (folder migrations in the root of the proj) with all the db versions. 
# pg db errror management
except psycopg2.DatabaseError as exeption:
    print ('database connection error')
    raise exeption 
#-----------------------------------


#LOGIN------------------------------
login = LoginManager(app)
login.login_view = 'login' # the assigned value 'login' is the function of the routes!! -> needed for login_required in the view functions
#-----------------------------------

# EMAIL SUPPORT CONFIGURATION ---------------------------
mail = Mail(app) # use the same mail-server configured for the log erorr (see below)

#LOG ERRORS TO A FILE------------------------------
if not app.debug:  # only run in production
    try:
        if not os.path.exists('logs'):  # if the specified path of the folder doesnt exists, it is created now
            os.mkdir('logs')
        
        # istance of the handler with its configuration (is possible to set a max dimension of the log file)
        file_Handler = RotatingFileHandler('logs/blog.log', maxBytes=10240, backupCount=10)  

        # custom formatting for the log messages. Here are: timestamp, logging level, message and the source file, line number from where the log entry originated.
        file_Handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_Handler.setLevel(logging.INFO) # level of the log reported (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        app.logger.addHandler(file_Handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')
    except:
        raise Exception('error in writing logs on a file')

#-------------------------------------------------------

#LOG ERRORS TO EMAIL------------------------------
if not app.debug:
    if app.config['MAIL_SERVER']:    # if not set, the whole service is dectivated
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:  # sets auth credentials
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        #istance of the handler which sends email and its configuration
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], ['MAIL_PORT']), 
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog error',
            credentials=auth, secure=secure) 
        
        mail_handler.setLevel(logging.ERROR)  # set the logs level that are sent

        app.logger.addHandler(mail_handler)   # here is defined how errors are handled in the app






# To test this feature: STMP debug server from python(fake server that accepts mail)
# to run the server run in another terminal the command: "python -m smtpd -n -c DebuggingServer localhost:8025"
# than set the flask envs:
#export MAIL_SERVER=localhost
#export MAIL_PORT=8025


# otherwise is possible to set a real email server and configure envs like this 
#export MAIL_SERVER=smtp.googlemail.com
#export MAIL_PORT=587
#export MAIL_USE_TLS=1
#export MAIL_USERNAME=<your-gmail-username>
#export MAIL_PASSWORD=<your-gmail-password>

#or 
#use SendGrid, which allows you to send up to 100 emails per day on a free account. 





#-------------------------------------------------------


from app import routes, models, errors # this goes at the bottom to avoid circular imports. here goes the modules that imports app

