from flask_migrate import Migrate
from data_handling import DataHandler

def deploy():
    from app import create_app
    from database import db
    from flask_migrate import upgrade, migrate, init, stamp
    
    app = create_app()
    app.app_context().push()
    db.create_all()
    Migrate(app, db)
    
    # Migrate database to latest
    init()
    stamp()
    migrate()
    upgrade()
    
    dh = DataHandler()
    dh.add_user('alice', "testtest")
    dh.add_user('bob', '12345678')
    u = dh.get_users()
    dh.post_message(authenticated_user=u[0], content="hei", recipient_ids=u)
    dh.post_message(authenticated_user=u[1], content="hei fra bob", recipient_ids=u)

    msgs = dh.get_messages(u[1])
    print(msgs)
    
deploy()
