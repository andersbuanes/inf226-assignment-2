from typing import List
from models import Message, User
from database import db
from utils import hash_password

class DataHandler():
    def get_messages(self, authenticated_user: User) -> List[Message]:
        result = authenticated_user.received_messages
        return result

    def get_users(self) -> List[User]:
        return User.query.all()
    
    def get_user(self, username) -> User:
        return User.query.filter_by(username=username).first()
    
    def get_search(self, query) -> List[Message]:
        return db.session.execute(db.select(Message).filter_by(message=query)).scalars()
    
    def add_user(self, username, password) -> None:
        hash, salt = hash_password(password)
        user = User(username=username, password=hash, salt=salt)
        db.session.add(user)
        db.session.commit()

    def post_message(self, authenticated_user: User, content, recipient_ids) -> None:
        msg = Message(
            sender=authenticated_user.id,
            content=content,
            recipients=recipient_ids
        )
        db.session.add(msg)
        db.session.commit()

