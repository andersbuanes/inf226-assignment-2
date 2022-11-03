from flask_migrate import Migrate
from data_handling import DataHandler

def deploy():
    from app import create_app
    from database import db
    from flask_migrate import upgrade, migrate, init, stamp
    
    app = create_app()
    app.app_context().push()
    db.create_all(bind_key='auth')
    db.create_all(bind_key='content')
    Migrate(app, db)
    
    # Migrate database to latest
    init()
    stamp()
    migrate()
    upgrade()
    
    dh = DataHandler()
    dh.add_user('alice', 'testtest')
    dh.add_user('bob', 'password123')
    
deploy()
