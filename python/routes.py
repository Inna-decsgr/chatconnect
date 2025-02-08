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


        # 사용자 데이터 업데이트
        if username:
            user.username = username
        if profile_message is not None:
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
    # 검색 기능에서 추가적으로 전달받을 id(선택적)
    filter_user_id = request.args.get('id', None)
    print('사용자 아이디', user_id)
    print('검색할 아이디', filter_user_id)

    try:
        # Messages 와 User 테이블 조인
        query = db.session.query(
            Messages,
            User.profile_image.label("profile_image"),  # 상대방의 프로필 이미지
            User.username.label("username")  # 상대방의 이름
        ).join(  # join은 두 테이블 연결, 여기서는 Messages랑 User 테이블을 연결
            User, db.or_(
                (Messages.sender_id == User.user_id),  # 보낸 사람과 조인
                (Messages.receiver_id == User.user_id)  # 받은 사람과 조인
            )
        ).filter( # SQL의 WHERE 조건과 동일
            # 메시지의 보낸 사람 또는 받는 사람이 현재 사용자(전달받은 user_id)인 메시지만 추려서 가져옴
            (Messages.sender_id == int(user_id)) | (Messages.receiver_id == int(user_id))
        )
        
        if filter_user_id:
            query = query.filter(
                db.or_(
                    db.and_(Messages.sender_id == user_id, Messages.receiver_id == filter_user_id),
                    db.and_(Messages.sender_id == filter_user_id, Messages.receiver_id == user_id)
                )
            )
            
        messages = query.order_by(Messages.created_at.desc()).all() # Messages.created_at을 기준으로 메시지를 오래된 순서대로 정렬한 후 모든 결과를 가져옴

        # SQLAlchemy 조인 결과로 인해 메시지 하나에 대해 두 개의 결과가 생성이 됨. 조인 조건에서 Messages.sender_id와 Messages.receiver_id가 모두 User.user_id와 조인되면서 동일한 메시지가 "보낸 사람의 정보"와 "받은 사람의 정보"를 기준으로 두 번 반환된다.
        # 조인 조건에서 sender_id와 receiver_id 모두 User.user_id와 조인되므로 Messages의 한 레코드가 두 번 반환된다.
        # 하나는 sender정보를 기준으로 다른 하나는 receiver 정보를 기준으로 반환해야됨



        # 메시지와 사용자 정보를 포함한 결과 반환
        result = []
        for msg, profile_image, username in messages:
            if msg.sender_id == int(user_id):
                # 내가 보낸 경우, 상대방(receiver)의 정보 반환
                receiver = User.query.filter_by(user_id=msg.receiver_id).first()
                result.append({
                    "chat_id": msg.chat_id,
                    "text": msg.text,
                    "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "receiver_id": msg.receiver_id,
                    "receiver_name": receiver.username,
                    "profile_image": receiver.profile_image
                })
            else:
                # 내가 받은 경우, 상대방(sender)의 정보 반환
                sender = User.query.filter_by(user_id=msg.sender_id).first()
                result.append({
                    "chat_id": msg.chat_id,
                    "text": msg.text,
                    "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "receiver_id": msg.sender_id,
                    "receiver_name": sender.username,
                    "profile_image": sender.profile_image
                })
        return jsonify(result), 200
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return jsonify({'message:' 'Failed to fetch messages'}), 500
    

    
# 해당 채팅방의 sender의 is_read를 모두 true로 설정하기
@app.route('/setisreadtrue/<chat_id>', methods=['POST'])
def set_is_read_true(chat_id):
    try:
        # POST 요청에서 user_id 가져오기
        data = request.json
        current_user_id = data.get('userid') # 클라이언트에서 전달된 user_id

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



# 친구 즐겨찾기에 추가하는 함수
@app.route('/addfavorite/<user_id>', methods=['POST'])
def add_favorite(user_id):
    try: 
        data = request.json # 요청 데이터로 부터 friendid 추출해서 favorite_id에 저장
        favorite_id = data['friendid']

        user = User.query.get(user_id)  # user_id에 해당하는 사용자를 User 모델에서 가져와 user에 저장
        favorite_user = User.query.get(favorite_id) # 즐겨찾기 할 친구의 아이디를 User 모델에서 가져와 favorite_user에 저장


        if user and favorite_user:  # 사용자와 즐겨찾기할 대상 모두 있을 경우
            if favorite_user in user.favorite_users:
                return jsonify({
                    'message': 'Favorite user already added',
                    'favorite_users': [u.user_id for u in user.favorite_users.all()]
                }), 400
            
            # 즐겨찾기에 추가
            user.favorite_users.append(favorite_user)  # user의 favorite_users에 favorite_user(즐겨찾기할 대상)을 append(추가)
            db.session.commit()  # 추가한 데이터 저장


            return jsonify({
                'message': 'Favorite user added successfully',
                'favorite_users': [u.user_id for u in user.favorite_users.all()]
            }), 200
        return jsonify({'message': 'User or favorite user not found'}), 404

    except Exception as e:
        print(f"Error add favorite_id: {e}")
        return jsonify({'message:' 'Failed to add favorite user'}), 500
    



# 친구 즐겨찾기 목록에서 해당 사용자 삭제하기
@app.route('/removefavorite/<user_id>', methods=['POST'])
def remove_favorite(user_id):
    try:
        data = request.json
        favorite_id = data['friendid']
        
        user= User.query.get(user_id)
        favorite_user = User.query.get(favorite_id)

        if user and favorite_user:
            if favorite_user in user.favorite_users:
                user.favorite_users.remove(favorite_user)
                db.session.commit()

            return jsonify({
                'message': 'Favorite user remove successfully',
                'favorite_users': [u.user_id for u in list(user.favorite_users)]
            }), 200
        return jsonify({'message': 'User or favorite user not found'}), 404
    
    except Exception as e:
        print(f"Error remove favorite_id: {e}")
        return jsonify({'message:' 'Failed to remove favorite user'}), 500


# 사용자가 즐겨찾기한 친구 목록 가져오기
@app.route('/getfavoritelist/<user_id>', methods=['GET'])
def get_favorites(user_id):
    user = User.query.get(user_id)
    if user:
        return [u.to_dict() for u in user.favorite_users]
    
    return []



# 검색한 키워드로 사용자 찾기
@app.route('/searchuser/<keyword>', methods=['GET'])
def get_search_user_result(keyword):
    # username에 keyword가 포함된 사용자 검색
    users = User.query.filter(User.username.ilike(f"%{keyword}%")).all()
    print('검색사용자', users)

    if users:
        return jsonify([{"id": user.user_id, "username": user.username} for user in users])
    
    return jsonify([]), 200


