def deploy():
    from app import create_app, db
    from flask_migrate import upgrade, migrate, init, stamp
    from models import User
    
    app = create_app()
    app.app_context().push()
    db.create_all()
    db.create_all(bind_key=[None, 'auth'])
    db.create_all(bind_key='messages')    
    
    # Migrate database to latest
    init()
    stamp()
    migrate()
    upgrade()
    
deploy()