from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from database import db
from login_manager import login_manager
from routes import routes

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tiny.db"
    db.init_app(app)
    app.register_blueprint(routes)
    login_manager.init_app(app)
    login_manager.login_view = "routes.login"
    return app

def setup_database(app):
    with app.app_context():
        db.create_all()
        