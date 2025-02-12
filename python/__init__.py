import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

load_dotenv() 


app = Flask(__name__)   
CORS(app, resources={r"/*": {"origins": "*"}})  


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysqlnote@localhost/chat'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') 

db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)  
jwt = JWTManager(app) 

# 🔥 Flask-SocketIO 설정
socketio = SocketIO(app, cors_allowed_origins="*")



# 📌 `routes.py`에서 `app`을 가져올 것이므로, import는 맨 아래에서 실행!
from python import routes