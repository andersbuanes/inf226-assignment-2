def deploy():
    from app import create_app
    from flask_migrate import upgrade, migrate, init, stamp
    from database import db
    
    # This should ensure tables are created but doesn't :)))))
    from models import User, Message, Announcement
    
    app = create_app()
    with app.app_context():
        db.create_all()
        db.create_all(bind_key=[None, "auth"])
        db.create_all(bind_key="content")
        
deploy()