from flask import Flask, abort, request, send_from_directory, make_response, render_template
import flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import login_required, login_user
from json import dumps
from apsw import Error
from markupsafe import escape
from login_manager import login_manager_init
from flask_sqlalchemy import SQLAlchemy
import config

inject = "'; insert into messages (sender,message) values ('foo', 'bar');select '"

migrate = Migrate()
bcrypt = Bcrypt()

app = Flask(__name__)

app.secret_key = 'mUh s3krit'
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_BINDS'] = config.SQLALCHEMY_BINDS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager_init(app)

import routes
with app.app_context():
    db.create_all()


