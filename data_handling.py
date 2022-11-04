from typing import List
from datetime import datetime
from sqlalchemy import or_
from sqlalchemy.orm import contains_eager

from models import Message, User
from database import db
from utils import hash_password

class DataHandler():
    def get_messages(self, authenticated_user: User) -> List[Message]:
        result = authenticated_user.received_messages + authenticated_user.send_messages
        result.sort(key=lambda x: x.timestamp)
        return result
    
    def get_message(self, message_id, authenticated_user: User) -> Message:
        return Message.query.join(Message.recipients).options(contains_eager(Message.recipients)) \
            .filter(or_(User.id == authenticated_user.id, Message.sender_id == authenticated_user.id)) \
            .filter(Message.id == message_id).first()
        

    def get_users(self) -> List[User]:
        return User.query.all()
    
    def get_user(self, username) -> User:
        return User.query.filter_by(username=username).first()
    
    def get_search(self, query, authenticated_user: User) -> List[Message]:
        return Message.query.join(Message.recipients).options(contains_eager(Message.recipients)) \
            .filter(or_(User.id == authenticated_user.id, Message.sender_id == authenticated_user.id)) \
            .filter(Message.content.contains(query)).order_by(Message.timestamp).all()
    
    def add_user(self, username, password) -> None:
        hash, salt = hash_password(password)
        user = User(username=username, password=hash, salt=salt)
        db.session.add(user)
        db.session.commit()

    def post_message(self, authenticated_user: User, content, recipient_ids) -> None:
        msg = Message(
            sender_id=authenticated_user.id,
            content=content,
            recipients=recipient_ids,
            timestamp=datetime.now().timestamp(),
        )
        db.session.add(msg)
        db.session.commit()

