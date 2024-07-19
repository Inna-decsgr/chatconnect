# ChattConnect

### 프로젝트 이름
ChattConnect

### 프로젝트 설명
ChattConnect는 사용자들이 친구들과 간편하게 채팅할 수 있는 웹 애플리케이션이다. 사용자는 회원가입 후 로그인하여 친구 목록을 관리하고, 실시간으로 메시지를 주고받을 수 있다. 이 애플리케이션은 Vue.js로 구성된 프론트엔드와 Flask를 기반으로 한 백엔드로 이루어져 있다.

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
채팅 어플리케이션을 구현하면서 발생한 문제들과 이를 해결하기 위해 한 방법들을 기술해보려고 한다.
* **문제 1: 로그인 유지가 되지 않음**

🫁 **문제 설명**: 사용자가 로그인이나 회원가입을 성공적으로 마친 후 다른 기능을 이용하다가 새로고침을 하면 로그인이 풀려 사용자가 로그아웃 상태가 되는 문제가 발생했다. 이로 인해 사용자는 로그인 상태를 지속적으로 유지할 수 없었다.  
🫁 **해결 방법**: 사용자가 로그인을 하면 사용자 정보를 localStorage에 저장하고, 새로고침 시 저장된 사용자 상태를 가져와 로그인 상태가 유지되도록 했다.  

(1) 상태 저장: `vuex-persistedstate` 플러그인을 사용하여 Vuex 상태가 변경될 때마다 자동으로 사용자 상태를 localStorage에 저장한다.  
store.js 파일에 플러그인을 추가하고 설정을 아래와 같이 수정했다.
```js
import createPersistedState from 'vuex-persistedstate';

export const store = new Vuex.Store({
  plugins: [ 
    createPersistedState({
      key: 'myApp', 
      paths: ['user'], 
    })
  ]
});
```

(2) 상태 복구:  애플리케이션이 로드될 때, localStorage에 저장된 토큰을 확인하고 사용자 데이터를 가져온다. store가 초기화될 때, localStorage 저장된 token이 있는지 확인한다. 사용자가 로그인할 때 SET_TOKEN 뮤테이션에서 `localStorage.setItem('access_token', token);` 토큰을 localstorage에 저장해뒀으니 로그인이 되었다면 아마 로컬 스토리지에 토큰이 저장되어있을 것이다.  토큰이 있으면 `fetchUserData()` 액션을 사용해서 사용자 데이터를 가져온다. 이렇게 하면 새로고침 후에도 사용자가 로귿인을 유지할 수 있다.
```js
if (store.state.token) {  
  store.dispatch('fetchUserData');
}
```

* **문제 2: SQLAlchemy 데이터베이스 오류**

🫁 **문제(1) 설명**: 애플리케이션을 실행할 때 콘솔에 다음과 같은 오류 메시지가 출력되었다. 
```
Error adding message: Class 'builtins.dict' is not mapped
```
테이블 이름을 Messages로 정의해두고 메시지를 추가할 때는 Message에 추가해 발생한 문제였다.  
🫁 **해결 방법**: 테이블 이름을 Messages로 일치시켰다.  

🫁 **문제(2) 설명**: 테이블 이름을 일치시키고 다시 실행하니 아래와 같은 에러가 발생했다.
```
Error adding message: (pymysql.err.ProgrammingError) (1146, "Table 'chat.message' doesn't exist")
```
tablename 속성 값이 실제 데이터베이스 테이블 이름과 달라서 발생한 문제였다.  
🫁 **해결 방법**: tablename 속성이 데이터베이스와 일치하지 않아서 Message를 Messages로 수정하고, Chats 테이블의 이름도 Chats로 수정했다. 그리고 `db.create_all()`을 run.py에 추가하여 어플리케이션이 실행되기 전에 테이블을 생성했다.  

🫁 **문제(3) 설명**: 테이블이 생성되도록 직접 코드를 추가하고 다시 실행해보니 이번엔 다른 에러가 발생했다.
```
Error adding message: (pymysql.err.DataError) (1265, "Data truncated for column 'chat_id' at row 1")
```
`Data truncated for column 'chat_id' at row 1` chat_id에 삽입하려는 데이터의 크기가 해당 열의 정의보다 커서 발생하는 에러이다. 데이터베이스 설계할 때 chat_id는 INT 타입으로 해두었는데 uuid로 chat_id를 생성하면서 chat_id가 길어져서 데이터 타입에 맞지 않게 된 것이다.  
🫁 **해결 방법**: 데이터 타입을 바꾸려고 하니 참조 관계 때문에 바꿀수가 없어서 우선 제약 조건을 모두 제거한 후에 참조하는 테이블과 참조되는 테이블의 chat_id 데이터 타입을 모두 VARCHAR(36)으로 변경해주었다.  
1 - 외래 키 참조 끊기
```
ALTER TABLE Messages DROP FOREIGN KEY Messages_Users_FK;
ALTER TABLE Messages DROP FOREIGN KEY Messages_Users_FK_1;
```
2 - 데이터 타입 변경
```
ALTER TABLE Messages MODIFY chat_id VARCHAR(36);
ALTER TABLE Chats MODIFY chat_id VARCHAR(36);
```
3 - 다시 관계 설정  
DBeaver로 다시 외래키 설정을 해줬더니 더 이상 에러가 발생하지 않고 정상적으로 작동하였고 실제로 메세지도 잘 전송되었다.

블로그에 문제 해결 과정을 더 자세히 작성해두었다.  
https://velog.io/@kimina/Vue.js%EB%A1%9C-%EC%B1%84%ED%8C%85-%EC%96%B4%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98-%EB%A7%8C%EB%93%A4%EA%B8%B0-%EC%8B%A4%EC%8B%9C%EA%B0%84-%EB%A9%94%EC%84%B8%EC%A7%80-%EC%A3%BC%EA%B3%A0-%EB%B0%9B%EA%B8%B01


#### 결론
vuex-persistedstate 플러그인을 활용해 로그인 상태 유지를 해결하며 클라이언트 측 상태 관리의 중요성을 배웠고, SQLAlchemy 오류 해결 과정에서 데이터베이스 설계와 구현의 일치가 중요함을 깨달았다. 이 경험을 바탕으로 사용자 경험을 향상시킬 자신감을 얻게 되었다.


### 사용 방법
🥲 백엔드 서버 실행  
프로젝트 디렉토리에서 `run.py` 파일을 실행하여 Flask 서버 시작하기  
`flask run`

🥲프론트엔드 어플리케이션 실행  
`npm run serve`


### 배포 링크
