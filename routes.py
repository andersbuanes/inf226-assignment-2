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
    make_response
)
import flask

from werkzeug.datastructures import WWWAuthenticate
from werkzeug.routing import BuildError

from flask_login import (
    login_user,
    login_required,
)

from models import Announcement, Message, User
from login_form import LoginForm
from data_handling import DataHandler
from app import app, db
from utils import is_safe_url, cssData, pygmentize
from login_manager import user_loader

dataHandler = DataHandler()

@app.route('/favicon.ico')
def favicon_ico():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/favicon.png')
def favicon_png():
    return send_from_directory(app.root_path, 'favicon.png', mimetype='image/png')

# Home route
@app.route('/')
@app.route('/index.html')
@login_required
def index_html():
    return send_from_directory(app.root_path,
                'index.html', mimetype='text/html')

def hash_password(password):
    # todo add hashing
    return password

def check_password_hash(stored_password_hash: str, inputed_password: str):
    return stored_password_hash == hash_password(inputed_password)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
        print(request.form)
    if form.validate_on_submit():
        # TODO: we must check the username and password
        username = form.username.data
        password = form.password.data
        u = User.query.filter_by(username=username).first()
        
        if u and check_password_hash(u.password, password):
            user = user_loader(username)
            
            # automatically sets logged in session cookie
            login_user(user)

            flask.flash('Logged in successfully.')

            next = flask.request.args.get('next')
    
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return flask.abort(400)

            return flask.redirect(next or flask.url_for('index'))
    return render_template('./login.html', form=form)

def to_dict(o):
    r = {}
    for e in o.__dict__.keys():
        if not e.startswith('_'):
            r[e] = o.__dict__[e]

    return r


# Search route
@app.get('/search')
def search():
    query = request.args.get('q') or request.form.get('q') or '*'
    m =  dataHandler.get_messages()
    return [to_dict(a) for a in m]
    #return dataHandler.get_search(query)

# Send route
@app.route('/send', methods=['POST','GET'])
@login_required
def send():
    try:
        sender = request.args.get('sender') or request.form.get('sender')
        message = request.args.get('message') or request.args.get('message')
        if not sender or not message:
            return f'ERROR: missing sender or message'

        dataHandler.post_simple_message(sender, message)

        return f'ok'
    except Error as e:
        return f'ERROR: {e}'

@app.get('/announcements')
def announcements():
    return dataHandler.get_announcments()

@app.get('/coffee/')
def nocoffee():
    abort(418)

@app.route('/coffee/', methods=['POST','PUT'])
def gotcoffee():
    return "Thanks!"

@app.get('/highlight.css')
def highlightStyle():
    resp = make_response(cssData)
    resp.content_type = 'text/css'
    return resp

