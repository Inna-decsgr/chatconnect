from flask import request, jsonify
from python import app, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from python.models import User, Messages
from python.__init__ import bcrypt
from datetime import datetime

# 사용자 등록 API
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')  # 요청에서 사용자 이름 가져오기
    password = request.json.get('password')  # 요청에서 비밀번호 가져오기

    # 사용자 이름 중복 확인
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"msg:" "이미 사용중인 아이디입니다."}), 400

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


# 사용자 프로필 정보 가져오기
@app.route('/get_profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)

    if user:
        return jsonify({
            "username": user.username,
            "userid": user.user_id
        }), 200
    
    return jsonify({"msg": "User not found!"}), 404


# 다른 모든 사용자들 정보 가져오기
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all() #OMR을 사용하여 모든 사용자 데이터 가져오기
        users_data = [user.to_dict() for user in users] 
        return jsonify(users_data), 200
        
    except Exception as e:
        print(f"Error fetching users: {e}")
        return jsonify({'message': 'Failed to fetch users'}), 500  # 에러 코드 수정
    

messages = []

# 메세지 보내기
@app.route('/messages', methods=['POST'])
def add_message():
    try :
        data = request.json
        chat_id = data['chat_id']
        sender_id = data['sender_id']
        sender_name = data['sender_name']
        receiver_id = data['receiver_id']
        receiver_name = data['receiver_name']
        text = data['text']
        created_at = datetime.now()

        new_message = Messages(
            chat_id= chat_id,
            sender_id= sender_id,
            sender_name= sender_name,
            receiver_id= receiver_id,
            receiver_name = receiver_name,
            text= text,
            created_at= created_at
        )
        db.session.add(new_message)
        db.session.commit()

        return jsonify(new_message.to_dict()), 201
    
    except Exception as e:
        print(f"Error adding message: {e}")
        return jsonify({'message': 'Failed to add message'}), 500
    

# 메시지 읽어오기
@app.route('/messages/<chat_id>', methods=['GET'])
def get_message(chat_id):
    try:
        messages = Messages.query.filter_by(chat_id=chat_id).order_by(Messages.created_at).all()
        return jsonify([msg.to_dict() for msg in messages]), 200
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return jsonify({'message:' 'Failed to fetch messages'}), 500

