from database import db
from sqlalchemy import Column, Integer, String

class User(db.Model):
    __bind_key__ = 'auth'
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(300), unique=True, nullable=False)
    salt = Column(String(300), unique=True, nullable=False)
    
    def __repr__(self):
        return "<User %r>" % self.username
    
#message_reciepent = db.Table('message_recipent',
                    #db.Column('message_id', db.Integer, db.ForeignKey('message.id')),
                    #db.Column('user_id', db.Integer, db.ForeignKey(User.id))
                    #)

class MessageUser(db.Model):
    __bind_key__ = 'content'
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return "<MessageUser %r>" % self.username

class Message(db.Model):
    __bind_key__ = 'content'
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    #recipients_id = db.Column(db.Integer, ForeignKey(User.id))
    #recipients = db.relationship(User)
    #recipients = db.relationship(User, secondary=message_reciepent, backref='recieved_messages')

    def __repr__(self):
        return f"<Message sent by {self.sender} recived by [{self.recipients}] {self.content}>"

