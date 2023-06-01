""" in this module are initialyzed all the objects that are used in the whole /app folder"""
from flask import Flask
from config import Config # environmental config

from flask_sqlalchemy import SQLAlchemy # database stuff
from flask_migrate import Migrate

from flask_login import LoginManager # Login


#FLASK SETTINGS---------------------
app = Flask(__name__)
app.config.from_object(Config) # import configs from the Class Config in the as-named module. the values are accessed with a dict-like statement (app.config['SECRET_KEY'])
#-----------------------------------


# DATABASE--------------------------
# to initialize a new db run on the terminal 'flask db upgrade':it will execute the script auto generated by the migration engine
db = SQLAlchemy(app)    # creation of the database obj
migrate = Migrate(app, db) # the migration engine, creates a repo (folder migrations in the root of the proj) with all the db versions. 
#-----------------------------------


#LOGIN------------------------------
login = LoginManager(app)
login.login_view = 'login' # the assigned value 'login' is the function of the routes!! -> needed for login_required in the view functions
#-----------------------------------


from app import routes, models # this goes at the bottom to avoid circular imports. here goes the modules that imports app

