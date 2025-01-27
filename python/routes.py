from flask import request, jsonify
from python import app, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from python.models import User, Messages, Chats
from python.__init__ import bcrypt
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os
from sqlalchemy import case


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일이 위치한 디렉토리 가져옴
UPLOAD_FOLDER = os.path.join(BASE_DIR, '../uploads')  # uploads 디렉토리의 절대 경로
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # 업로드 폴더 지정. 나중에 파일 저장 시 이 경로를 사용한다.
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 업로드할 수 있는 파일 확장자 제한

def allowed_file(filename):
    # 파일 이름에 .(확장자 구분자)이 포함되어 있는지 확인하기
    # 파일 이름에서 마지막 . 이후의 부분(확장자)를 가져옴
    # 확장자가 ALLOWED_EXTENSIONS에 포함되어 있는지 확인 후 true or false를 반환
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 정적 파일 경로 설정, /uploads/<filename> 경로로 요청이 들어오면 실행
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    try:
        # send_from_directory : 지정된 디렉토리(UPLOAD_FOLDER)에서 요청된 파일을 찾아 클라이언트에게 반환
        # 예를 들어 app.config['UPLOAD_FOLDER'] 가 C:\Users\user\Desktop\projects\Vue.js\chatconnect\uploads로 설정되어 있으면 이 디렉토리에서 filename을 찾아 반환
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        print(f"오류 발생: {e}")  # 에러 로그 출력
        return jsonify({"msg": "파일을 찾을 수 없습니다."}), 404


# 사용자 등록 API
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    id = request.form.get('id')
    password = request.form.get('password')
    email = request.form.get('email')
    phonenumber = request.form.get('phonenumber')
    profile_image = request.files.get('profileImage')

    print(f"Request files: {request.files}")  # 업로드된 파일 확인
    print(f"Form data: {request.form}")  # 폼 데이터 확인

    # 사용자 아이디 중복 확인
    existing_user = User.query.filter_by(id=id).first()
    if existing_user:
        return jsonify({"msg":"이미 사용중인 아이디입니다."}), 400
    
    # 비밀번호 해시 처리
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    

    # 프로필 이미지 처리
    if profile_image and allowed_file(profile_image.filename):
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
            
        filename = secure_filename(profile_image.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        profile_image.save(save_path)
        profile_image = f"/uploads/{filename}"  # URL 경로로 변환
    else:
        profile_image = None
    
    # 새로운 사용자 객체 생성
    new_user = User(
        username=username,
        id=id,
        password=hashed_password,
        email=email,
        phonenumber=phonenumber,
        profile_image=profile_image
    ) 
    db.session.add(new_user)  # 데이터베이스 세션에 추가
    db.session.commit()  # 세션 커밋(저장)
    
    return jsonify(new_user.to_dict()), 201  # to_dict 메서드가 User 객체를 딕셔너리로 변환




# 사용자 로그인 API
@app.route('/login', methods=['POST'])
def login():
    id = request.json.get('id')  # 요청에서 사용자 이름 가져오기
    password = request.json.get('password')  # 요청에서 비밀번호 가져오기
    
    user = User.query.filter_by(id=id).first()  # 사용자 조회
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.user_id)  # JWT 토큰 생성
        return jsonify({
            "access_token": access_token,
            "user": user.to_dict()  # User 객체를 딕셔너리로 변환하여 포함
        }), 200 
    
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
            "userid": user.user_id,
            "email": user.email,
            "phonenumber": user.phonenumber,
            "profile_image": user.profile_image,
            "profile_message": user.profile_message
        }), 200
    
    return jsonify({"msg": "User not found!"}), 404


# 사용자 프로필 업데이트하기
@app.route('/updateprofile/<int:userid>', methods=['POST'])
def update_profile(userid):
    try:
        # 사용자 조회
        user = User.query.get(userid)
        if not user:
            return jsonify({"msg": "사용자를 찾을 수 없습니다"}), 404

        # 요청에서 데이터 추출
        username = request.form.get('username')
        profile_message = request.form.get('profile_message')
        profile_image = request.files.get('profile_image')

        print(f"Username: {username}")
        print(f"Profile Message: {profile_message}")
        print(f"Profile Image: {profile_image}")


        # 사용자 데이터 업데이트
        if username:
            user.username = username
        if profile_message:
            user.profile_message = profile_message

        # 프로필 이미지 처리
        if profile_image and allowed_file(profile_image.filename):
            # 기존 이미지 삭제
            if user.profile_image:
                old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(user.profile_image))
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            # 새 이미지 저장
            filename = secure_filename(profile_image.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            profile_image.save(file_path)

            # 이미지 경로 업데이트
            user.profile_image = f"/uploads/{filename}"

        # 데이터베이스 업데이트
        db.session.commit()

        return jsonify({
            "msg": "프로필이 성공적으로 업데이트되었습니다.",
            "user": {
                "username": user.username,
                "profile_message": user.profile_message,
                "profile_image": user.profile_image,
            }
        }), 200
    except Exception as e:
        print(f"오류 발생: {e}")
        return jsonify({"msg": "프로필 업데이트 중 오류가 발생했습니다."}), 500






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
    


# 메세지 보내기
messages = []
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

        chat = Chats.query.get(chat_id)
        if not chat:
            # 처음 대화하는 상대라면 새 채팅방 생성
            new_chat = Chats(chat_id=chat_id,  # UUID를 사용해 고유한 ID 생성
                    user1_id=sender_id,
                    user2_id=receiver_id,
                    created_at=created_at)
            db.session.add(new_chat)
            db.session.commit()
            chat_id = new_chat.chat_id  # 생성된 chat_id 사용

        # 메시지 저장
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
    

# 특정 채팅방의 메시지 읽어오기
@app.route('/messages/<chat_id>', methods=['GET'])
def get_message(chat_id):
    try:
        # Messages와 User 테이블 조인해서 receiver의 profile_image 가져오기
        messages = db.session.query(
            Messages,
            User.profile_image.label("receiver_profile_image") # 조인된 User 테이블의 profile_image를 receiver_profile_image라는 별칭으로 반환함
            # receiver_profile_image는 실제 데이터베이스에 존재하는 필드는 아니지만 SQLAlchemy가 반환 데이터를 다룰 때 임의로 지정된 이름을 사용하기 때문에 결과 반환할 때 사용할 수 있음
            # 여기서!! 조인 조건은 sender_id로 했는데 실제 가져오는 건 receiver의 프로필 이미지를 가져오게 보이는 이유는 쿼리의 다른 부분에서 조인 조건과 반환 데이터 정의가 정확히 설정되었기 때문이다.
            # label은 반환 데이터에 이름만 붙일 뿐 실제로 가져오는 데이터는 조인 조건에 따라 결정되므로 이부분에서 반환되는 데이터는 보낸 사람의 profile_image이다

        ).join(
            # Messages.sender_id와 User.user_id를 기준으로 조인
            # Messages 테이블의 각 행에 대해 메시지를 보낸 사람과 일치하는 정보(sender_id와 일치하는 사용자의 정보)를 User 테이블로 부터 가져와서 조인 결과에 추가함
            # 실제 조인 쿼리 결과에는 모든 데이터(Messages 테이블 데이터와 조인된 User 데이터. 즉 sender_id로 조인하나 receiver_id로 조인하나에 상관없이 Message와 관련된 receiver_id, sender_id 정보가 모두)가 포함되어 있다.
            # 따라서 메시지의 상대방 정보는 이미 조인된 결과에 포함되어있으므로 조인을 통해 보낸 사람의 정보를 가져왔지만 각 메시지에서 대해 상대방의 정보도 추론할 수 있는 상태가 되게 된다.
            # 즉, Messages.sender_id를 기준으로 User 테이블과 조인하지만 결과적으로는 메시지의 상대방(receiver) 정보를 추론할 수 있는 상태가 되는 것
            # 결과적으로 조인된 결과에는 sender_id 즉, 보낸 사람의 정보가 포함되게 된다.
            User, Messages.sender_id == User.user_id
        ).filter(
            # Messages 테이블에서 요청된 chat_id에 해당하는 메시지만 필터링함
            Messages.chat_id == chat_id 
        ).order_by(Messages.created_at.asc()).all() # 메시지는 created_at을 기준으로 오래된 순서로 정렬됨

        # 메시지 반환
        result = [
            {
                **msg.to_dict(),
                "receiver_profile_image": receiver_profile_image
            }
            for msg, receiver_profile_image in messages
        ]

        return jsonify(result), 200

    except Exception as e:
        print(f"Error fetching messages: {e}")
        return jsonify({'message:' 'Failed to fetch messages'}), 500


# 대화목록에서 보여줄 마지막 메세지와 대화방에 대한 정보 가져오기
@app.route('/lastmessage/<user_id>', methods=['GET'])
def get_last_message(user_id):
    try:
        # Messages 와 User 테이블 조인
        messages = db.session.query(
            Messages,
            case( # case((조건, 반환값), else_=기본값)
                (Messages.sender_id == int(user_id), User.profile_image),  # 메세지를 보낸 사람이 현재 사용자라면 받는 사람의 프로필 이미지를 가져옴
                else_=None
            ).label("receiver_profile_image"),
            case(
                (Messages.receiver_id == int(user_id), User.profile_image),  # 메시지를 받는 사람이 현재 사용자라면 보낸 사람의 프로필 이미지를 가져옴
                else_=None
            ).label("sender_profile_image") # 쿼리 결과에 별칭 붙임
        ).join(  # join은 두 테이블 연결, 여기서는 Messages랑 User 테이블을 연결
            User, Messages.receiver_id == User.user_id  
            # 사용자가 로그인을 하게 되면 항상 보내는 입장이 되고 다른 사용자들은 항상 받는 사람이 되기 때문에 받는 사람에 대한 사용자 정보만 가져오도록 함
            # 이때 Messages.sender_id == User.user_id도 비교하게 되면 두 테이블을 조인하게 되면서 한 메시지에 대해 결과가 2개가 나오게 되고 원치않는 정보까지 반환될 수 있음
            # 헷갈리면 안되는게 receiver_id와 현재 사용자(전달받은)를 비교하는게 아니라 User 테이블의 있는(모든 사용자 중) 사용자와 일치하는 지 비교하는 것임
        ).filter( # SQL의 WHERE 조건과 동일
            # 메시지의 보낸 사람 또는 받는 사람이 현재 사용자(전달받은 user_id)인 메시지만 추려서 가져옴
            (Messages.sender_id == int(user_id)) | (Messages.receiver_id == int(user_id))  
        ).order_by(Messages.created_at.desc()).all() # Messages.created_at을 기준으로 메시지를 오래된 순서대로 정렬한 후 모든 결과를 가져옴

        # SQLAlchemy 조인 결과로 인해 메시지 하나에 대해 두 개의 결과가 생성이 됨. 조인 조건에서 Messages.sender_id와 Messages.receiver_id가 모두 User.user_id와 조인되면서 동일한 메시지가 "보낸 사람의 정보"와 "받은 사람의 정보"를 기준으로 두 번 반환된다.
        # 조인 조건에서 sender_id와 receiver_id 모두 User.user_id와 조인되므로 Messages의 한 레코드가 두 번 반환된다.
        # 하나는 sender정보를 기준으로 다른 하나는 receiver 정보를 기준으로 반환해야됨



        # 메시지와 사용자 정보를 포함한 결과 반환
        result = [
            {
                **msg.to_dict(), # 쿼리 결과인 messages를 순회하며 to_dict 메서드로 메시지 정보를 딕셔너리 형식로 변환
                "profile_image": sender_profile_image if msg.receiver_id == int(user_id) else receiver_profile_image,
                # 메시지의 보낸 사람(sender) 또는 받는 사람(receiver)에 따라 프로필 이미지 설정
                # 내가 메시지를 받은 사람이라면(if msg.receiver_id == int(user_id)) 보낸 사람의 프로필 이미지를(sender_profile_image)를 그 반대로 내가 메시지를 보낸 사람이라면 받은 사람의 프로필 이미지를 (receiver_profile_image) profile_image에 저장
                "username": (
                    msg.sender_id == int(user_id) and User.query.filter_by(user_id=msg.receiver_id).first().username
                ) or User.query.filter_by(user_id=msg.sender_id).first().username
                # User 테이블에서 상대방의 username을 가져옴
                # 내가 메시지를 보냈다면 User 테이블에서 메시지를 받은 상대방(msg.receiver_id)와 일치하는 user_id를 가진 사용자의 username을 반환하고 내가 메시지를 받았다면 보낸 사람(msg.sender_id)와 일치하는 user_id를 가진 사용자의 username을 찾아서 반환
            }
            for msg, receiver_profile_image, sender_profile_image in messages
        ]
        result = make_json_serializable(result)

        return jsonify(result), 200
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return jsonify({'message:' 'Failed to fetch messages'}), 500
    

# JSON으로 변환할 수 없는 데이터를 변환
# set, dict, list, tuple 또는 SQLAlchemy 객체를 재귀적으로 JSON 직렬화 가능한 형식으로 변환
def make_json_serializable(data):
    """모든 데이터를 JSON 직렬화 가능하게 변환"""
    if isinstance(data, set):
        return list(data)  # set -> list 변환
    elif isinstance(data, dict):
        return {k: make_json_serializable(v) for k, v in data.items()}  # dict 내부 순환
    elif isinstance(data, list):
        return [make_json_serializable(i) for i in data]  # list 내부 순환
    elif isinstance(data, tuple):  # SQLAlchemy 반환된 tuple 처리
        return [make_json_serializable(i) for i in data]
    elif hasattr(data, "__dict__"):  # SQLAlchemy 객체 처리
        return make_json_serializable(vars(data))
    else:
        return data
    

    
# 해당 채팅방의 sender의 is_read를 모두 true로 설정하기
@app.route('/setisreadtrue/<chat_id>', methods=['POST'])
def set_is_read_true(chat_id):
    try:
        # POST 요청에서 user_id 가져오기
        data = request.json
        current_user_id = data.get('userid') # 클라이언트에서 전달된 user_id

        print('채팅방아이디', chat_id)
        print('사용자 아이디', current_user_id)

        if not current_user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        # 해당 채팅방(chat_id)에서 현재 사용자가 받은 메시지(receiver의 메시지)
        messages = Messages.query.filter(
            Messages.chat_id == chat_id, # 해당 채팅방
            Messages.receiver_id == current_user_id,  # 현재 사용자가 받은 메시지
            Messages.is_read == False  # 읽지 않은 메시지만
        ).update({"is_read": True})  # 읽음 처리

        db.session.commit() # 변경 사항 저장

        return jsonify({'message': messages}), 200
    
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return jsonify({'message:' 'Failed to fetch messages'}), 500




