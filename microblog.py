""" fhe 'flask run' comamnd executes this module, which inports the app itself and the database"""
from app import app, db 


# this is added so the app can run calling this file with python and can set port and debug mode
# without this statement, run in the root folder the command flask run
#app.run(port=5001, debug=True)



# shell context is used only to run command in the shell without import all every time
from app.models import Users, Posts
@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'Users':Users, 'Posts':Posts} # the key of the dict is the alias of how the item is called in the shell
