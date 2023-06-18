# run flask app to a specific host and port:
```
flask run -h localhost -p 3000
```

# docker container: 
- build: build the container from the Dockerfile without fancy option
```
docker build -t blog_docker .   
```
- to run it: create and run a contaier with the app reachable from localhost:5000. --rm option delete it after it closes
```
docker run -p 5000:5000 -d --name microblog --rm blog_docker
```

# custom decorator 
example create a decorator that allows only some users to access a view

the function that creates the custom decorator
```
def <decorator_name>(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        .... body of the function ...
    return decorated_view
```

the view with the decorator
```
    @app.route("/<route>"):
@login_required
@<decorator_name>
def function_name():
    return "Hello admin"
```

# deal with role permission
## add roles and different levels of permission in login 
add an admin login account who can access some views other users cant

- in the 'app/__init__'
```
from flask_principal import Principal

# load the extension
principals = Principal(app)
```
```
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user
    # Add the UserNeed to the identity
    if hasattr(current_user, 'employee_id'):
        identity.provides.add(UserNeed(current_user.employee_id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'position'):
        # for role in current_user.role:
        identity.provides.add(RoleNeed(str(current_user.position)))

   admin_permission = Permission(RoleNeed('admin'))
   ```

- in the 'app/routes'
```
@app.route("/admin-restricted"):
@login_required
@admin_permission.require(http_exception=403)
def admin_resource():
    return "Hello admin"
```

# connection to remote postgres db

```
def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')
    
    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        # this string describes all info for psycopg2 to connect to the database
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')

```

# PAGINATION
sqlalchemy provide a method paginate() where is possible to specify the number of results at time
it takes 3 arguments: 
    - page = page number
    - per_page = item per page
    - error_out = error flag  for out of range requests ( 404)

returns a Pagination object<br>
can be configured in the config.py

# EMAIL SUPPORT
## password reset
install packages flask-email and pyjwt for the mail and contents management
### use of tokens 
a single use link is sent to the email address, to be sure the link is valid are used tokens <br>
**JSON web tokens** (JWT) are most used for this 
run --> pip install pyjwt
```
import jwt
# token creation 
token = jwt.encode( value to send eg a dict, 'my-secret', algorithm='HS256')

# read token
jwt.decode(token, 'my-secret', algorithms=['HS256'])
```
does not created an encrypted token, but a signed payload(not modificable payload)


# LANG SUPPORT 

a config file is needed to define languages to use. see the babel.cfg file
the command below automatically extract the marked text (with _()and _l() functions) to a .pot file 
``` 
pybabel extract -F babel.cfg -k _l -o messages.pot . 
```
The pybabel extract command reads the configuration file given in the -F option, then scans all the code and template files in the directories that match the configured sources, starting from the directory given in the command (the current directory or . in this case). By default, pybabel will look for _() as a text marker, but I have also used the lazy version, which I imported as _l(), so I need to tell the tool to look for those too with the -k _l. The -o option provides the name of the output file.
the file can be deleted and recreated running the command again. it can be done when new text is added to the code

### generating code languages
this command uses messages.pot as ref to generate a lang catalog i the given directory
```
pybabel init -i messages.pot -d app/translations -l it
```
creating catalog app/translations/it/LC_MESSAGES/messages.po based on messages.pot
than the message.po file created must be edited with transaltion manually

### compiling messages.po
the file must be compilet to be used runtime with the command:
```
pybabel compile -d app/translations
```
this adds a messages.mo file in the same folder

## update with other text
add _() and _l() to new text and run:
```
pybabel extract -F babel.cfg -k _l -o messages.pot .
pybabel update -i messages.pot -d app/translations
```
the extract is the same than above, the merges the new message.po file jus created
than is possible to edit angain and re compile it with the command above
