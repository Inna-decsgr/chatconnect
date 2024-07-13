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
    sender_name = db.Column(db.String(36), nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    receiver_name = db.Column(db.String(36), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'chat_id': self.chat_id,
            'sender_id': self.sender_id,
            'sender_name': self.sender_name,
            'receiver_id': self.receiver_id,
            'receiver_name': self.receiver_name,
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
    

# to_dict 메서드는 객체의 속성을 딕셔너리 형태로 변환하는 역할을 한다.
# 1. 데이터베이스에서 가져온 모델 객체를 JSON 형태로 변환하기 위해 사용, API 응답으로 보내거나 클라이언트에서 사용할 수 있도록 데이터 구조를 변경한다.
# 2. 객체의 속성을 딕셔너리로 쉽게 변환하면, 데이터 조작이나 API 응답 생성 시 유용하다
# 3. 어떤 속성이 어떤 값을 가지는지 명확히 나타내어, 코드 가독성 높아진다