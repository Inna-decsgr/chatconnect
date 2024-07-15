import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

load_dotenv() 


app = Flask(__name__)   
CORS(app, resources={r"/*": {"origins": "*"}})  


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mariadb@localhost/chat'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') 

db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)  
jwt = JWTManager(app) 


from python import routes 