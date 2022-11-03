from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, event
from sqlalchemy_utils import create_database, database_exists

db = SQLAlchemy()

def validate_databases():
    engines = [
        create_engine('sqlite:///content.db'),
        create_engine('sqlite:///auth.db'),
    ]
    
    for engine in engines:
        if not database_exists(engine.url):
            create_database(engine.url)