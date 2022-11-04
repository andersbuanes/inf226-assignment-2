from flask import Flask

from config import Config
from database import db
from login_manager import login_manager
from routes import routes

import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    filename='application.log',
    filemode='w')

def setup_database(app):
    with app.app_context():
        db.create_all()
        
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(routes)
    login_manager.init_app(app)
    login_manager.login_view = "routes.login"
    db.init_app(app)
    migrate.init_app(app)
    bcrypt.init_app(app)
    
    return app
