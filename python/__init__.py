import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

load_dotenv()  # .env 파일 로드해서 환경 변수 사용할 수 있도록 설정


app = Flask(__name__)   # Flask 어플리케이션 인스턴스 생성
CORS(app, resources={r"/*": {"origins": "*"}})  # 모든 경로와 모든 출처 허용

# 데이터베이스 URL 설정(MYSQL 연결)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mariadb@localhost/chat'
# JWT 비밀 키 설정 (토큰 생성 시 사용)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # 비밀 키 설정

db = SQLAlchemy(app) # SQLAlchemy 데이터베이스 객체 생성
bcrypt = Bcrypt(app)  # Bcrypt 객체 생성(비밀번호 해시용)
jwt = JWTManager(app) # JWT 관리 객체 생성


from python import routes  # routes를 import하여 라우트를 등록