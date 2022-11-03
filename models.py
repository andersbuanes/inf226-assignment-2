from database import db
from sqlalchemy import Column, Integer, String, event

class User(db.Model):
    __bind_key__ = 'auth'
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(300), unique=True, nullable=False)
    
    def __repr__(self):
        return "<User %r>" % self.username
    
@event.listens_for(User.__table__, 'after_create')
def create_users(*args, **kwargs):
    db.session.add(User('bob', 'banananas'))
    db.session.add(User('alice', 'password123'))
    db.session.commit()
    
class Message(db.Model):
    __bind_key__ = 'content'
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender = Column(String(80), nullable=False)
    message = Column(String(500), nullable=False)

    def __repr__(self):
        return "<Message %r>" % self.message


class Announcement(db.Model):
    __bind_key__ = 'content'
    __tablename__ = 'announcement'

    id = Column(Integer, primary_key=True)
    auther = Column(String(80), nullable=False)
    text = Column(String(500), nullable=False)

    def __repr__(self):
        return "<Announcement %r>" % self.text
