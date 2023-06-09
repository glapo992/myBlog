from flask import render_template
from app import app, db


# is a normal view like those on routes
@app.errorhandler(404)
def not_found_errro(error):
    return render_template('404.html', title = 'err 404'), 404  # returns also a status code of the error 



@app.errorhandler(500)
def internal_errro(error):
    # err 500 can be caused by a db error 
    # To make sure any failed database sessions do not interfere with any database accesses triggered by the template, a session rollback is issued. 
    # This resets the session to a clean state.
    db.session.rollback()  
    return render_template('500.html', title = 'err 500'), 500