import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

load_dotenv()  # .env 파일 로드해서 환경 변수 사용할 수 있도록 설정


app = Flask(__name__)    # Flask 어플리케이션 인스턴스 생성
CORS(app, resources={r"/*": {"origins": "*"}})   # 모든 경로와 모든 출처 허용



# 데이터베이스 URL 설정(MYSQL 연결)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysqlnote@localhost/chat'
# JWT 비밀 키 설정 (토큰 생성 시 사용)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') 

db = SQLAlchemy(app)  # SQLAlchemy 데이터베이스 객체 생성
bcrypt = Bcrypt(app)   # Bcrypt 객체 생성(비밀번호 해시용)
jwt = JWTManager(app)  # Bcrypt 객체 생성(비밀번호 해시용)

# 🔥 Flask-SocketIO 설정
socketio = SocketIO(app, cors_allowed_origins="*")



# `routes.py`에서 `app`을 가져올 것이므로, import는 맨 아래에서 실행!
from python import routes