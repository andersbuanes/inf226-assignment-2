from http import HTTPStatus
from sqlite3 import DataError, DatabaseError, IntegrityError, InterfaceError
from apsw import Error
from flask import (
    abort,
    render_template,
    redirect,
    flash,
    url_for,
    send_from_directory,
    request,
    session,
    make_response,
    Blueprint
)
import flask
import bcrypt

from werkzeug.datastructures import WWWAuthenticate
from werkzeug.routing import BuildError

from flask_login import (
    login_user,
    logout_user,
    login_required,
)
from auth_handling import AuthHandler

from login_form import LoginForm
from data_handling import DataHandler
from models import User
from register_form import RegisterForm
from utils import is_safe_url, cssData, pygmentize
from login_manager import user_loader

data_handler = DataHandler()
auth_handler = AuthHandler()
routes = Blueprint('routes', __name__)

@routes.route('/favicon.ico')
def favicon_ico():
    return send_from_directory(routes.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@routes.route('/favicon.png')
def favicon_png():
    return send_from_directory(routes.root_path, 'favicon.png', mimetype='image/png')

# Home route
@routes.route('/')
@routes.route('/index.html')
@login_required
def index_html():
    return send_from_directory(routes.root_path,
                'index.html', mimetype='text/html')

def hash_password(password):
    salt = bcrypt.gensalt()
    password_hashed = bcrypt.hashpw(password, salt)
    
    return (password_hashed, salt)

def check_password_hash(stored_password_hash: str, inputed_password: str):
    return stored_password_hash == hash_password(inputed_password)

@routes.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    if form.is_submitted():
        print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
        print(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = auth_handler.get_user(username)
        
        if user:
            return redirect(url_for('routes.register'))
        auth_handler.create_user(username, password)
                
        return redirect(url_for('routes.login'))
    return render_template('register.html')

# Login route
@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
        print(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        u = User()
        
        if u: #and check_password_hash(u.password, password):
            user = user_loader(username)
            print(user)
            
        login_user(user)
        print('User authenticated: %b' % user.is_authenticated)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')

        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(url_for('index'))
    return render_template('./login.html', form=form)

def to_dict(o):
    r = {}
    for e in o.__dict__.keys():
        if not e.startswith('_'):
            r[e] = o.__dict__[e]

    return r

@routes.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect('/')

# Search route
@routes.get('/search')
@login_required
def search():
    query = request.args.get('q') or request.form.get('q') or '*'
    m =  data_handler.get_search(query)
    return [to_dict(a) for a in m]

from web_models import UserWebSchema
@routes.get('/user')
def get_user():
    users =  data_handler.get_users()
    schema = UserWebSchema(many=True)
    result = schema.dumps(users)
    return result

# Send route
@routes.post('/send')
@login_required
def send():
    try:
        users =  data_handler.get_users()
        print(users)
        sender = request.args.get('sender') or request.form.get('sender')
        message = request.args.get('message') or request.args.get('message')
        if not sender or not message:
            return f'ERROR: missing sender or message'

        data_handler.post_message(users[1], message, recipient_ids=[1,2])

        return f'ok'
    except Error as e:
        return f'ERROR: {e}'

@routes.get('/highlight.css')
def highlightStyle():
    resp = make_response(cssData)
    resp.content_type = 'text/css'
    return resp

