from flask_login import LoginManager, UserMixin
from werkzeug.datastructures import WWWAuthenticate
from http import HTTPStatus
from flask import abort, Flask
from base64 import b64decode

from config import SQLALCHEMY_BINDS, SQLALCHEMY_DATABASE_URI

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

def login_manager_init(app: Flask):
    # The secret key enables storing encrypted session data in a cookie (make a secure random key for this!)
    app.secret_key = 'mY s3kritz'
    app.config.update(
        SECRET_KEY='',
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=True,
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_BINDS=SQLALCHEMY_BINDS,
        SQLALCHEMY_TRACK_MODIFICATIONS=True
    )
    login_manager.init_app(app)
    login_manager.login_view = "routes.login"

# Add a login manager to the app
users = {'alice' : {'password' : 'password123', 'token' : 'tiktok'},
         'bob' : {'password' : 'bananas'}
         }

# Class to store user info
# UserMixin provides us with an `id` field and the necessary
# methods (`is_authenticated`, `is_active`, `is_anonymous` and `get_id()`)
class User(UserMixin):
    pass


# This method is called whenever the login manager needs to get
# the User object for a given user id
@login_manager.user_loader
def user_loader(user_id) -> User or None:
    if user_id not in users:
        return

    # For a real app, we would load the User from a database or something
    user = User()
    user.id = user_id
    return user


# This method is called to get a User object based on a request,
# for example, if using an api key or authentication token rather
# than getting the user name the standard way (from the session cookie)
@login_manager.request_loader
def request_loader(request) -> User or None:
    # Even though this HTTP header is primarily used for *authentication*
    # rather than *authorization*, it's still called "Authorization".
    auth = request.headers.get('Authorization')

    # If there is not Authorization header, do nothing, and the login
    # manager will deal with it (i.e., by redirecting to a login page)
    if not auth:
        return

    (auth_scheme, auth_params) = auth.split(maxsplit=1)
    auth_scheme = auth_scheme.casefold()
    if auth_scheme == 'basic':  # Basic auth has username:password in base64
        (uid,passwd) = b64decode(auth_params.encode(errors='ignore')).decode(errors='ignore').split(':', maxsplit=1)
        print(f'Basic auth: {uid}:{passwd}')
        u = users.get(uid)
        if u: # and check_password(u.password, passwd):
            return user_loader(uid)
    elif auth_scheme == 'bearer': # Bearer auth contains an access token;
        # an 'access token' is a unique string that both identifies
        # and authenticates a user, so no username is provided (unless
        # you encode it in the token – see JWT (JSON Web Token), which
        # encodes credentials and (possibly) authorization info)
        print(f'Bearer auth: {auth_params}')
        for uid in users:
            if users[uid].get('token') == auth_params:
                return user_loader(uid)
    # For other authentication schemes, see
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication

    # If we failed to find a valid Authorized header or valid credentials, fail
    # with "401 Unauthorized" and a list of valid authentication schemes
    # (The presence of the Authorized header probably means we're talking to
    # a program and not a user in a browser, so we should send a proper
    # error message rather than redirect to the login page.)
    # (If an authenticated user doesn't have authorization to view a page,
    # Flask will send a "403 Forbidden" response, so think of
    # "Unauthorized" as "Unauthenticated" and "Forbidden" as "Unauthorized")
    abort(HTTPStatus.UNAUTHORIZED, www_authenticate = WWWAuthenticate('Basic realm=inf226, Bearer'))
