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