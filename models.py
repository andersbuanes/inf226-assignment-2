from database import db
from sqlalchemy import Column, Integer, String

class User(db.Model):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(300), unique=True, nullable=False)
    salt = Column(String(300), unique=True, nullable=False)
    send_messages = db.relationship("Message", back_populates="sender")
    
    def __repr__(self):
        return "<User %r>" % self.username
    
    def get_messages(self):
        return self.received_messages

    def to_dict(self):
        return {
                'username': self.username,
                'id': self.id,
                }
    
message_reciepent = db.Table('recipients',
                    db.Column('message_id', db.Integer, db.ForeignKey('message.id')),
                    db.Column('user_id', db.Integer, db.ForeignKey(User.id)),
                    )

class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = Column(Integer, db.ForeignKey(User.id))
    sender = db.relationship(User, back_populates="send_messages")
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.String(20), nullable=False)
    recipients = db.relationship(User, secondary='recipients', backref='received_messages')
    
    def to_dict(self):
        a = {
            "id": self.id,
            "sender": self.sender.username,
            "content": self.content,
            "time": self.timestamp,
            "recipients": [r.to_dict() for r in self.recipients],
        }
        return a

    def __repr__(self):
        return f"<Message sent by {self.sender} content: '{self.content}'>"
