from python import db
from datetime import datetime, timezone

# 사용자 즐겨찾기 관계를 저장할 중간 테이블
favorite_users = db.Table(
    'favorite_users',
    db.Column('user_id', db.Integer, db.ForeignKey('Users.user_id'), primary_key=True),
    db.Column('favorite_id', db.Integer, db.ForeignKey('Users.user_id'), primary_key=True)
)



# User 모델 정의
class User(db.Model):
    __tablename__ = 'Users'  # 테이블 이름
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    id = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phonenumber = db.Column(db.String(20), unique=True, nullable=False)
    profile_image = db.Column(db.String(255))
    profile_message = db.Column(db.String(255))
    favorite_users = db.relationship(
        'User',
        secondary=favorite_users,
        primaryjoin=(favorite_users.c.user_id == user_id),
        secondaryjoin=(favorite_users.c.favorite_id == user_id),
        backref=db.backref('favorited_by', lazy='dynamic'),
        lazy='dynamic'
    )

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'id': self.id,
            'email': self.email,
            'phonenumber': self.phonenumber,
            'profile_image': self.profile_image,
            'profile_message': self.profile_message,
            'favorite_users': [user.user_id for user in self.favorite_users] 
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
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            'chat_id': self.chat_id,
            'sender_id': self.sender_id,
            'sender_name': self.sender_name,
            'receiver_id': self.receiver_id,
            'receiver_name': self.receiver_name,
            'text': self.text,
            'created_at': self.created_at.isoformat(),
            'is_read': self.is_read
        }
    

# Chat 모델 정의
class Chats(db.Model):
    __tablename__ = 'Chats'  # 테이블 이름
    chat_id = db.Column(db.String(36), primary_key=True)
    user1_id = db.Column(db.Integer, nullable=False)
    user2_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'chat_id': self.chat_id,
            'user1_id': self.user1_id,
            'user2_id': self.user2_id,
            'created_at': self.created_at
        }
    

# to_dict 메서드는 객체의 속성을 딕셔너리 형태로 변환하는 역할을 한다.
# 1. 데이터베이스에서 가져온 모델 객체를 JSON 형태로 변환하기 위해 사용, API 응답으로 보내거나 클라이언트에서 사용할 수 있도록 데이터 구조를 변경한다.
# 2. 객체의 속성을 딕셔너리로 쉽게 변환하면, 데이터 조작이나 API 응답 생성 시 유용하다
# 3. 어떤 속성이 어떤 값을 가지는지 명확히 나타내어, 코드 가독성 높아진다