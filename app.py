import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()  # .env 파일 로드해서 환경 변수 사용할 수 있도록 설정


app = Flask(__name__)   # Flask 어플리케이션 인스턴스 생성
CORS(app)  # 모든 경로에 대해 CORS를 허용

# 데이터베이스 URL 설정(MYSQL 연결)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mariadb@localhost/chat'
# JWT 비밀 키 설정 (토큰 생성 시 사용)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # 비밀 키 설정

db = SQLAlchemy(app) # SQLAlchemy 데이터베이스 객체 생성
bcrypt = Bcrypt(app)  # Bcrypt 객체 생성(비밀번호 해시용)
jwt = JWTManager(app) # JWT 관리 객체 생성


# User 모델 정의
class User(db.Model):
    __tablename__ = 'Users'  # 테이블 이름
    user_id = db.Column(db.Integer, primary_key=True)  # 사용자 ID(기본키)
    username = db.Column(db.String(50), unique=True, nullable=False) # 사용자 이름(고유값, NULL 불가)
    password = db.Column(db.String(255), nullable=False)  # 비밀번호 (NULL 불가)
    nickname = db.Column(db.String(50), nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)

# 테이블 생성 (이미 생성했으면 생략 가능)

# 사용자 등록 API
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')  # 요청에서 사용자 이름 가져오기
    password = request.json.get('password')  # 요청에서 비밀번호 가져오기
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # 비밀번호 해시 처리
    
    new_user = User(username=username, password=hashed_password)  # 새로운 사용자 객체 생성
    db.session.add(new_user)  # 데이터베이스 세션에 추가
    db.session.commit()  # 세션 커밋(저장)
    
    return jsonify({"msg": "User registered successfully!"}), 201  # 성공 메시지 반환


# 사용자 로그인 API
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')  # 요청에서 사용자 이름 가져오기
    password = request.json.get('password')  # 요청에서 비밀번호 가져오기
    
    user = User.query.filter_by(username=username).first()  # 사용자 조회
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.user_id)  # JWT 토큰 생성
        return jsonify(access_token=access_token), 200  # 토큰 반환
    
    return jsonify({"msg": "Invalid username or password"}), 401  # 실패 메시지 반환

# 사용자 정보 등록 API
@app.route('/update_profile', methods=['POST'])
@jwt_required()
def update_profile():
    current_user = get_jwt_identity()  # 현재 사용자 ID 가져오기
    nickname = request.json.get('nickname')
    profile_image = request.json.get('profile_image')

    user = User.query.get(current_user)
    if user:
        user.nickname = nickname
        user.profile_image = profile_image
        db.session.commit()
        return jsonify({"msg": "Profile Updated Successfully!"}), 200
    
    return jsonify({"msg" : "User not found!"}), 404

# 사용자 프로필 정보 가져오기
@app.route('/get_profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)

    if user:
        return jsonify({
            "username": user.username
        }), 200
    
    return jsonify({"msg": "User not found!"}), 404



if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(port=5000, debug=True)  # 디버그 모드로 FLASK 서버 실행
