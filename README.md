# ChattConnect

### 프로젝트 이름
ChattConnect

### 프로젝트 설명
ChattConnect는 사용자들이 친구들과 간편하게 채팅할 수 있는 웹 애플리케이션입니다. 사용자는 회원가입 후 로그인하여 친구 목록을 관리하고, 실시간으로 메시지를 주고받을 수 있습니다. 이 애플리케이션은 Vue.js로 구성된 프론트엔드와 Flask를 기반으로 한 백엔드로 이루어져 있습니다.

### 사용 기술
* 프론트엔드
  * **Vue.js**: 사용자 인터페이스 구축
  * **Vuex**: 상태 관리
  * **Vue Router**: 라우팅 관리
  * **Axios**: HTTP 클라이언트
  * **Bootstrap**: UI 스타일링
* 백엔드
  * **Flask**: 웹 프레임워크
  * **Flask-SQLAlchemy**: ORM을 통한 데이터베이스 작업
  * **Flask-JWT-Extended**: JWT 기반 인증 처리
  * **Flask-CORS**: Cross-Origin Resource Sharing 지원
  * **Flask-Bcrypt**: 비밀번호 해싱
  * **MySQL**: 데이터베이스


### 구현 사항
* 프론트엔드
  * **회원가입 및 로그인**: 새로운 사용자가 계정을 생성하거나 기존 사용자 로그인
  * **프로필 관리**: 로그인한 사용자 정보 확인, 로그아웃
  * **친구 목록**: 친구 목록 조회하고, 친구에게 메시지 전송하기
  * **실시간 채팅**: 선택한 친구와의 채팅방에서 메시지를 주고받기
* 백엔드
  * **사용자 등록 API**: `/register` 엔드포인트를 통해 새로운 사용자 등록
  * **로그인 API**: 사용자 로그인할 때 JWT 토큰 발급받아 인증 절차 거치기
  * **프로필 조회 API**: 현재 사용자의 프로필 정보 반환
  * **모든 사용자 조회 API**: 데이터베이스에 등록된 모든 사용자 정보 가져오기
  * **메시지 전송 API**: 사용자가 메시지를 전송하고, 특정 채팅의 메시지 조회
 
### 주요 내용
* 프론트엔드
  * **사용자 인터페이스**
    * 회원가입: 사용자로부터 이름과 비밀번호를 입력받아 /register API로 요청
    * 로그인: 사용자 인증을 위해 /login API에 요청하여 JWT 토큰을 전달받음
  * **상태 관리**
    * Vuex 사용: 사용자 정보, 토큰, 친구 목록 등의 상태 관리
    * SET_USER, SET_TOKEN, CLEAR_AUTH_DATA, SET_FRIENDS 등의 뮤테이션 정의
  * **친구 목록**
    * 모든 사용자 조회: 로그인 후 /users API를 호출하여 친구 목록을 가져오기
    * 채팅 시작: 친구 목록에서 친구를 선택해서 채팅 시작
  * **메시지 기능**
    * 메시지 전송 및 수신: 사용자가 메시지를 입력하고 전송하면 /messages API를 호출하여 메시지를 저장하고, 특정 채팅방의 메시지를 조회

* 백엔드
  * **사용자 인증**
    * 회원가입 API (/register): 사용자 이름과 비밀번호를 받아 데이터베이스에 새로운 사용자 정보를 저장
    * 로그인 API (/login): 사용자 인증 후 JWT 토큰을 생성하여 반환
    * 프로필 조회 API (/get_profile): 로그인한 사용자 정보를 반환
  * **사용자 목록 관리**
    * 모든 사용자 조회 API (/users): 등록된 모든 사용자 정보 가져오기
  * **메시지 처리**
    * 메시지 전송 API (/messages): 클라이언트에서 전송된 메시지 데이터베이스에 저장
    * 메시지 조회 API (/messages/<chat_id>): 특정 채팅방의 메시지 기록 가져오기
  * **데이터베이스 설계**
    * User 모델: 사용자 정보 (ID, 이름, 비밀번호 해시 등) 저장
    * Messages 모델: 각 메시지의 송신자, 수신자, 내용 저장
    * Chats 모델: 채팅방 정보 (사용자 ID) 관리
    

### 문제 해결


#### 결론


### 사용 방법
🥲 백엔드 서버 실행  
프로젝트 디렉토리에서 `run.py` 파일을 실행하여 Flask 서버 시작하기  
`flask run`

🥲프론트엔드 어플리케이션 실행  
`npm run serve`


### 배포 링크
