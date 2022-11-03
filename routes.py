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

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)
from data_handling import DataHandler
from login_form import LoginForm
from register_form import RegisterForm
from models import User
from utils import check_password_hash, is_safe_url, cssData, pygmentize
from login_manager import user_loader

data_handler = DataHandler()
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

@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.is_submitted():
        print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
        print(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = data_handler.get_user(username)
        
        if user:
            return redirect(url_for('routes.register'))
        data_handler.add_user(username, password)
                
        return redirect(url_for('routes.login'))
    return render_template('register.html', form=form)

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
        
        u = data_handler.get_user(username)
        
        if u and check_password_hash(u.password, password, u.salt):
            user = user_loader(username)
            
            login_user(user)

            flask.flash('Logged in successfully.')

            next = flask.request.args.get('next')

            if not is_safe_url(next):
                return flask.abort(400)

            return flask.redirect(next or '/')
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

@routes.get('/search')
@login_required
def search():
    query = request.args.get('q') or request.form.get('q') or '*'
    m =  data_handler.get_search(query)
    return [to_dict(a) for a in m]

from web_models import MessageWebSchema, UserWebSchema
@routes.get('/user')
def get_user():
    users =  data_handler.get_users()
    schema = UserWebSchema(many=True)
    result = schema.dumps(users)
    return result

# Get user messages
@routes.get('/message')
@login_required
def get_messages():
    try: 
        schema = MessageWebSchema()
        user =  data_handler.get_user(current_user.get_id())
        users =  data_handler.get_users()

        messages = data_handler.get_messages(user)
        messages = [a.to_dict() for a in messages]
        mapped_result = [schema.dump(a) for a in messages]

        return mapped_result
    except Error as e:
        return f'ERROR: {e}'

# Send route
@routes.post('/send')
@login_required
def send():
    if request.json == None:
        return 'Error'

    try:
        user =  data_handler.get_user(current_user.get_id())
        users =  data_handler.get_users()
        recipients = request.json['recipients']
        recipient_names = recipients

        recipient_ids = [user for user in users if user.username in recipient_names]
                
        message = request.json['message']
        if not recipient_ids or not message:
            return f'ERROR: missing recipients or message'

        data_handler.post_message(user, message, recipient_ids)

        return f'ok'
    except Error as e:
        return f'ERROR: {e}'

@routes.get('/highlight.css')
def highlightStyle():
    resp = make_response(cssData)
    resp.content_type = 'text/css'
    return resp

