from app import app, db


# shell context to run command in the shell without import all every time
from app.models import Users, Posts
@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'Users':Users, 'Posts':Posts} # the key of the dict is the alias of how the item is called in the shell
