from python import db
from datetime import datetime, timezone


# User 모델 정의
class User(db.Model):
    __tablename__ = 'Users'  # 테이블 이름
    user_id = db.Column(db.Integer, primary_key=True)  # 사용자 ID(기본키)
    username = db.Column(db.String(50), unique=True, nullable=False) # 사용자 이름(고유값, NULL 불가)
    password = db.Column(db.String(255), nullable=False)  # 비밀번호 (NULL 불가)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username
        }
    
# Messages 모델 정의
class Messages(db.Model):
    __tablename__ = 'Messages'  # 여기서 'messages'로 설정
    message_id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(36), nullable=False)
    sender_id = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'chat_id': self.chat_id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'text': self.text,
            'created_at': self.created_at.isoformat()
        }
    

# Chat 모델 정의
class Chats(db.Model):
    __tablename__ = 'Chats'  # 테이블 이름
    chat_id = db.Column(db.String(36), primary_key=True)
    user1_id = db.Column(db.Integer, nullable=False)
    user2_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'chat_id': self.chat_id,
            'user1_id': self.user1_id,
            'user2_id': self.user2_id,
        }