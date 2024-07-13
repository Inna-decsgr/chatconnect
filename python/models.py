from python import db

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