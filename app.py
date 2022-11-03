from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

from database import db, validate_databases
from login_manager import login_manager
from routes import routes
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
    validate_databases()
    migrate.init_app(app)
    bcrypt.init_app(app)
    
    return app