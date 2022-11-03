from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from database import db
from login_manager import login_manager
from routes import routes
from config import SQLALCHEMY_BINDS

def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="Muh sektrix"
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tiny.db"
    app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS
    db.init_app(app)
    app.register_blueprint(routes)
    login_manager.init_app(app)
    login_manager.login_view = "routes.login"
    return app

def setup_database(app):
    with app.app_context():
        db.create_all()
        
