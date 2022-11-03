from models import User
from database import db

class AuthHandler():
    def get_user(self, username):
        return User.query.filter_by(username=username).first()
    
    def get_credentials(self, username):
        return db.session.execute(db.select(User).filter_by(username=username)).select(User.password)
    
    def create_user(self, username, password):
        user = User(
            username=username,
            password=password,
        )
        
        db.session.add(user)
        db.session.commit()