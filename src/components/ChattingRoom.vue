<template>
  <div id="app">
    <div>
      <ChatTopBar />
    </div>
    <div class="chat-container p-3" ref="chatContainer">
      <div v-for="(group, groupIndex) in messages" :key="groupIndex">
        <!-- 날짜별로 표시-->
        <p class="bg-gray-800 bg-opacity-5 text-center w-[160px] mx-auto my-3 text-xs py-[6px] rounded-xl text-gray-600">
          <i class="fa-regular fa-calendar"></i>
          {{group.date}} {{ group.day }}
        </p>
        <!--날짜별로 메시지 반복-->
        <div v-for="(minuteGroup, minuteIndex) in group.groupedMinutes" :key="minuteIndex" class="mb-2">
        <!--쉽게 생각하면 receiver_id, 수신자가 7이고 보내는 사람이 8이라고 치자. 그럼 sender_id와 user.userid는
        8로 같을수밖에 없잖아. 현재 로그인된 사용자가 메시지를 보낼테니까. 근데 우리가 채팅방을 만들때 같은 방을 
        공유하게 만들어뒀으니까 7이 sender가 될수도 receiver가 될수도 있고 8이 sender가 될수도 receiver가 될 수도 있잖아 그치?
        데이터베이스 보면서 이해하면 더 잘될거야. receiver_id가 userid와 같은것만 따로 모아서 왼쪽 정렬하고
        receiver_id와 userid가 다른것만 모아서 오른쪽 정렬하는거야! 그냥 야매로 생각하자면 현재 로그인된
        사용자가 sender가 되어서 오른쪽에 보여야하는거잖아. 그러니까 반대로 생각해서 receiver_id와 userid
        가 같은 것만 골라서 왼쪽정렬하면 v-else했을때 반대의 경우가 다 오른쪽 정렬되니까 그런거라고 생각해.
        미래의 나야...과거의 내가 멍청해서 미안 허허허 내가 고쳤어! 현재 사용자와 sender_id가 
        같지 않으면 수신자라는 거니까 msg.receiver_id === user.userid에서 아래와 같이 바꿈!ㅎㅎ-->
          <!-- 시간순으로 정렬된 메시지를 표시 -->
          <div v-for="(msg, msgIndex) in minuteGroup" :key="msgIndex">
            <div class="message-wrapper" :class="msg.sender_id === user.userid ? 'sender-wrapper' : 'receiver-wrapper'">
              <div class="message-container">
                <div class="flex">
                  <!-- ✅ 첫 번째 메시지에만 프로필 이미지 표시 -->
                  <img v-if="isFirstAfterReply(minuteGroup, msgIndex, minuteGroup) && msg.sender_id !== user.userid" :src="msg.receiver_profile_image ? `http://localhost:5000${msg.receiver_profile_image}` : '/images/사용자 프로필.png'" class="w-[40px] h-[40px] object-cover rounded-[16px]">
                  <div class="pl-3">
                  <!-- ✅ 첫 번째 메시지에만 사용자 이름 표시 -->
                    <p class="text-[12px] mb-[3px]" v-if="isFirstAfterReply(minuteGroup, msgIndex, minuteGroup) && msg.sender_id !== user.userid">
                      {{ msg.sender_name }}
                    </p>
                    <div class="flex">
            
                      <!-- ✅ 수신자(receiver)일 경우 -->
                      <div v-if="msg.sender_id !== user.userid" class="flex">
                        <div>
                          <p :class="['message', 'receiver', msgIndex === 0 ? 'has-tail' : '', !isFirstAfterReply(minuteGroup, msgIndex, minuteGroup) ? 'ml-[39px]' : '']">
                            {{ msg.text }}
                          </p>
                        </div>
                        <!-- ✅ 마지막 메시지일 경우 시간 표시 -->
                        <p v-if="isLastMessageInSenderGroup(minuteGroup, msgIndex, minuteGroup)" class="time">
                          {{ msg.created_at }}
                        </p>
                      </div>

                      <!-- ✅ 발신자(sender)일 경우 -->
                      <div v-if="msg.sender_id === user.userid" class="flex items-center">
                        <div class="info-wrapper" :class="{'abc' : isLastMessageInSenderGroup(minuteGroup, msgIndex, minuteGroup) && !msg.is_read }">
                          <p v-if=" !msg.is_read && 
                            !readindicator[msg.message_id] &&
                            !isrealtime" 
                            class="unread-indicator"
                            :class="msgIndex !== minuteGroup.length - 1 ? 'mt-[14px]' : 'mt-[2px]'">1</p>
                          <!-- ✅ 마지막 메시지에만 시간 표시 -->
                          <p v-if="isLastMessageInSenderGroup(minuteGroup, msgIndex, minuteGroup)" class="time">
                            {{ msg.created_at }}
                          </p>
                        </div>
                        <div>
                          <p :class="['message', 'sender', msgIndex === 0 ? 'has-tail' : '']">
                            {{ msg.text }}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="flex">
      <input 
        type="text" 
        class="basis-5/6 text-xs p-3 outline-none" 
        v-model="newMessage" 
        placeholder="메시지 입력" 
        @keyup.enter="sendmessage"
        @input="newMessage = $event.target.value"
      >
      <!--@input 이벤트는 사용자가 입력 필드에 값을 입력하거나 변경할 때마다 트리거됨. 
        입력한 값을 실시간으로 감지하면서 추가로 공백 제거 작업을 처리하기 위해서 사용.
        Vue에서는 v-model과 동일한 동작으로 수행하기 때문에 데이터 간의 양방향 바인딩을 설정하는 역할을 함.
        v-model을 사용했지만 추가적인 데이터 처리(공백 제거, 유효성 검사)가 필요할 때 유용.
      -->
      <button 
        class="text-xs basis-1/6" 
        :disabled="!newMessage.trim()"
        :class="newMessage ? 'bg-[#f7e330] hover:bg-[#ffd966]' : 'bg-gray-200 text-gray-400 cursor-not-allowed'"
        @click="sendmessage">전송</button>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { v4 as uuidv4 } from 'uuid';
import { chatformatTime } from '@/utils/chatformatTime';
import ChatTopBar from './ChatTopBar.vue';
import socket from "../utils/socket";
import axios from 'axios';

export default {
  components: {
    ChatTopBar
  },
  data() {
    return {
      newMessage: '',
      messages: [],
      chatId: null,
      readindicator: [],  // 각 메세지의 읽음 상태를 저장. {메세지 아이디: true or false}
      userinroom: [],  // 채팅방에 들어와있는 사용자들 아이디
      isrealtime: null  // 지금 실시간으로 대화중인지 아닌지
    }
  },
  created() {
    this.loadUserandMessages();
  },
  props: { 
    friendId: {
      type: String,
      required: true
    },
    friendName: {
      type: String,
      required: true
    },
    friendImage: {
      type: String,
      required: false
    }
  },
  computed: {
    ...mapState(['user'])
  },
  mounted() {
    socket.on("new_message", (data) => {
      console.log("📩 서버에서 받은 실시간 메시지:", data);
      console.log("🚀 새 메시지가 감지됨! `get_messages` 실행");
      socket.emit("get_messages", { chat_id: this.chatId });
    })

    // ✅ 서버에서 채팅 내역 수신
    socket.on("get_message", (data) => {
      console.log('채팅 아이디', this.chatId);
      console.log('메세지들222222', data);
      if (!data || data.length === 0) {
        console.error("❌ 메시지 데이터가 없음!", data);
        return;
      }
      this.messages = [];
      data.forEach(msg => this.addMessageToChat(msg));
    });

    socket.on("set_is_read_true", (data) => {
      console.log("📢 읽음 표시 소켓 이벤트 데이터", data);

      // ✅ 받은 데이터를 이용해 현재 메시지의 읽음 상태 업데이트
      data.messages.forEach((updatedMsg) => {
        this.readindicator[updatedMsg.message_id] = updatedMsg.is_read
      });
    });

    socket.on('handle_join_room', (data) => {
      console.log("받은 데이터:", data);

      // 받은 데이터에서 채팅방 ID 가져오기
      const key = Object.keys(data)[0];
      const userList = data[key] || [];

      if (!this.userinroom) {
        this.userinroom = {};
      }
      // this.userinroom이 객체가 아닐 경우 초기화
      if (!this.userinroom[key]) {
        this.userinroom[key] = [];
      }

      // 기존 목록 유지하면서 새로운 사용자 추가(중복 제거)
      const currentUsers = new Set(this.userinroom[key]);  // 기존 사용자 목록
      userList.forEach(user => currentUsers.add(user));  // 새로운 사용자 추가

      this.userinroom[key] = [...currentUsers];  // Set을 다시 배열로 변환
      console.log("현재 채팅방 사용자 목록:", this.userinroom[key]);

      // 실시간 채팅 여부 확인
      if (
        this.userinroom[key].includes(Number(this.friendId)) &&
        this.userinroom[key].includes(Number(this.user.userid))
      ) {
        this.isrealtime = true;
        console.log("실시간 채팅중?", this.isrealtime);
      } else {
        this.isrealtime = false;
      }
    });

    socket.on('handle_leave_room', (data) => {
      console.log('채팅방 나간 후', data);

      const key = Object.keys(data)[0];
      const userList = data[key] || [];
      
      if (this.userinroom[key]) {
        // 나간 사람 해당 채팅방에서 삭제
        this.userinroom[key] = this.userinroom[key].filter(id => id !== userList);
        
        // 만약 방에 아무도 없으면 해당 키 삭제
        if (this.userinroom[key].length === 0) {
          delete this.userinroom[key];
        }
      }
      this.isrealtime = false
    })
  },
  updated() {
    this.scrollToBottom();
  },
  methods: {
    async loadUserandMessages() {
      await this.$store.dispatch('fetchUserData'); 

      if (this.user && this.user.userid) {
        this.chatId = this.getChatId();
        socket.emit("get_messages", { chat_id: this.chatId }); // ✅ 서버에 메시지 요청
      } else {
        console.error('User is not defined or userid is missing');
      }

      this.setIsReadTrue(this.chatId);
    },
    getChatId() {
      const ids = [this.user.userid, this.friendId].sort();
      const chatKey = `chatId_${ids.join('_')}`;  
      let chatId = localStorage.getItem(chatKey); 

      if (!chatId) {  
        chatId = uuidv4();   
        localStorage.setItem(chatKey, chatId); 
      }
      return chatId;
    },
    scrollToBottom() {
      const container = this.$refs.chatContainer;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    },
    sendmessage() {
      if (this.newMessage.trim()) {
        const timestamp = new Date().toISOString();
        const tempId = `temp-${Date.now()}`;

        const message = {
          id: tempId,
          chat_id: this.chatId,
          sender_id: this.user.userid,
          sender_name: this.user.username,
          receiver_id: this.friendId,
          receiver_name: this.friendName,
          text: this.newMessage,
          created_at: timestamp,
          realtime: this.isrealtime
        };

        console.log('보낼 메세지', message);

         // ✅ 내가 보낸 메시지를 화면에 즉시 추가
        this.addMessageToChat(message);

         // ✅ 서버에 메시지 전송
        socket.emit("message", message);
        socket.emit("get_messages", { chat_id: this.chatId });
          
        this.newMessage = '';  // 메세지 보내고 input 비우기
      }
    },
    addMessageToChat(data) {
      // 날짜 키와 요일 계산
      const daysOfWeek = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"];
      const dateObj = new Date(data.created_at);
      const year = dateObj.getFullYear();
      const month = dateObj.getMonth() + 1;
      const day = dateObj.getDate();
      const dateKey = `${year}년 ${month}월 ${day}일`;
      const dayOfWeek = daysOfWeek[dateObj.getDay()];

      // 시간 + 분 키 생성
      const hour = dateObj.getHours().toString().padStart(2, "0");
      const minute = dateObj.getMinutes().toString().padStart(2, "0");
      const minuteKey = `${hour}:${minute}`;

      // 새로운 메시지 포맷
      const formattedMessage = {
        ...data,
        created_at: chatformatTime(data.created_at)
      };
      
      const senderId = formattedMessage.sender_id;
      // 기존 그룹에서 메시지를 추가할 해당 날짜 키를 찾음
      const groupIndex = this.messages.findIndex(group => group.date === dateKey);

      if (groupIndex !== -1) {
        // 해당 날짜 그룹이 이미 있으면 그 그룹의 groupedMinutes(시간 그룹) 배열을 groupedMinutes에 저장
        const groupedMinutes = this.messages[groupIndex].groupedMinutes;

        if (!groupedMinutes[minuteKey]) {
          // 해당 날짜는 있는데 해당 시간이 없을 경우 새로 생성
          groupedMinutes[minuteKey] = {};
        }

        // 해당 sender_id 그룹이 없으면 새로 생성
        if (!groupedMinutes[minuteKey][senderId]) {
          groupedMinutes[minuteKey][senderId] = [];
        }

        // 해당 sender_id 그룹에 메시지 추가
        groupedMinutes[minuteKey][senderId].push(formattedMessage);
      } else {
        // 해당 날짜 그룹이 없으면 새 그룹을 생성 후 메세지 추가
        this.messages.push({
          date: dateKey,
          day: dayOfWeek,
          groupedMinutes: {
            [minuteKey]: {
              [senderId]: [formattedMessage]
            }
          }
        });
      }

      // 추가된 메세지를 시간순으로 정렬
      this.sortMessages();
      this.$nextTick(() => this.scrollToBottom());  // 스크롤 자동 이동
    },
    sortMessages() {
      // 시간 -> 아이디별로 그룹되어있는 메세지들을 다시 하나로 합쳐서 시간순서대로 정렬
      // 이렇게 안하면 각자 아이디밑에 추가되기 때문에 대화가 안되고 거의 독백이 됨ㅠ
      this.messages.forEach(group => {
        group.groupedMinutes = Object.fromEntries(
          Object.entries(group.groupedMinutes).map(([minuteKey, senderGroups]) => [
            minuteKey,
            Object.values(senderGroups)  // sender_id 별 메시지 배열들 가져오기
              .flat() // 하나의 배열로 합치기
              .sort((a, b) => new Date(a.created_at) - new Date(b.created_at))  // 시간순 정렬
          ])
        )
      })
    },
    isFirstAfterReply(msgGroup, msgIndex, minuteGroup) {
      // msgGroup 내에서 첫번째 메시지이거나, 중간에 상대방이 답장을 해서 시간은 안지났지만 다시 보여줘야할 때는 true 반환
      if (msgIndex === 0) return true; // 원래 첫 번째 메시지는 무조건 표시

      const prevMsg = minuteGroup[msgIndex - 1]; // 이전 메시지
      return prevMsg && prevMsg.sender_id !== msgGroup[msgIndex].sender_id;
    },
    isLastMessageInSenderGroup(msgGroup, msgIndex, minuteGroup) {
      // msgGroup에서 마지막 메세지이거나 다음 메시지가 다른 sender라면 true 반환
      // 시간이 마지막 메세지에만 표시되도록 해뒀는데 상대방이 같은 시간 안에 답장함녀 그 메세지가 마지막이 되면서 시간을 뺏어감ㅠ
      if (msgIndex === msgGroup.length - 1) return true; // 그룹 내 마지막 메시지는 무조건 true

        const nextMsg = minuteGroup[msgIndex + 1]; // 다음 메시지
        return !nextMsg || nextMsg.sender_id !== msgGroup[msgIndex].sender_id;
    },
    updateMessageInChat(data) {
      console.log("📩 서버에서 받은 메시지를 기존 메시지와 비교하여 업데이트:", data);

      for (let group of this.messages) {
        for (let minuteKey in group.groupedMinutes) {
          let minuteGroup = group.groupedMinutes[minuteKey];
          const index = minuteGroup.findIndex(msg => msg.id === `temp-${data.created_at}`);

          if (index !== -1) {
            minuteGroup[index] = data; // 서버에서 받은 데이터로 업데이트
            return;
          }
        }
      }
      this.addMessageToChat(data);
    },
    async unreadmessages() {
      if (!this.user || !this.user.userid) return;
      socket.emit("get_unread_message", { user_id: this.user.userid });
      // 클라이언트에서 서버에 "나 안 읽은 메세지 개수 좀 알려주라"라고 emit으로 요청을 보내게 되고 서버의 @socketio.on("get_unread_message")라우트가 실행됨. get_unread_message 라우트 내에서 안 읽은 메시지를 조회 후 다시 emit("get_unread_message", result)를 실행하게 되면 다시 클라이언트에서(MainBar)의 socket.on("get_unread_message")가 자동 실행되면서 수신함
    },
    async setIsReadTrue(chatid) {
      try {
        // this.chatId랑 this.userid
        //  {{ this.chatId }}{{ this.user.userid }}
        console.log('서버에 읽음 처리 이벤트 요청');
        socket.emit("set_is_read_true", { chat_id: chatid, userid: this.user.userid })

        const response = await axios.post(`http://localhost:5000/setisreadtrue/${chatid}`, {
          userid: this.user.userid
        });
        console.log('is_read를 true로', response.data);
        
        // 특정 채팅방만 업데이트하도록 Vuex 상태 변경
        this.$store.commit("set_specific_unread_message", {
          chatid: chatid, 
          userid: this.user.userid
        });

        // ✅ 서버에서 최신 unread 개수 가져오기
        this.unreadmessages();

      } catch (error) {
        console.error('Error setting is_read:', error.response.data);
      }
    }
  }
}
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  height: 100vh; /* 화면 전체를 채움 */
}

.chat-container {
  height: 500px;
  flex: 1;
  overflow-y: auto;
  background: #bad0e5;
  padding: 10px;
}

.sender-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-end;  /* 메세지 오른쪽 정렬*/
  position: relative;
}

.receiver-wrapper {
  display: flex;
  flex-direction: column;
  position: relative;
}

.message-container {
  display: flex;
  flex-direction: row;
  align-items: flex-end;  /* 시간이랑 말풍선 수직 정렬 */
  max-width: 70%;
  margin-bottom: 6px;
}

.sender {
  background-color: #f7e330; 
  border-radius: 4px;
  padding: 6px 10px;
  font-size: 12px;
  position: relative;
  word-break: break-word;
  text-align: left;
}


.receiver {
  background-color: white;
  border-radius: 4px;
  padding: 6px 10px;
  position: relative;
  margin-right: 7px; 
  font-size: 12px;
}

.info-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 1px;
  margin-top: 2px;
  padding-right: 2px;
}

.receiver-wrapper .time {
  color: #555555;
  font-size: 11px;
  padding-top: 14px;
}
.sender-wrapper .time {
  color: #555555;
  font-size: 11px;
  width: 50px;
  margin-top: 12px;
}


/* 읽지 않은 메시지 (1)를 시간 위에 작은 크기로 표시 */
.sender-wrapper .unread-indicator {
  font-size: 11px;
  color: #f7e330;
  text-align: center;
  padding-right: 3px;

}

.abc .time {
  margin-top: -5px;
}


.sender.has-tail::after,
.receiver.has-tail::after {
  content: '';
  position: absolute;
  width: 0;
  height: 0;
}

.sender.has-tail::after {
  border-left: 13px solid #f7e330;
  border-top: 2px solid transparent;
  border-bottom: 10px solid transparent;
  right: -10px; 
  top: 8px;
}

.receiver.has-tail::after {
  border-right: 13px solid white;
  border-top: 2px solid transparent;
  border-bottom: 10px solid transparent;
  left: -10px;
  top: 8px;
}

/* 스크롤바 전체 영역 */
::-webkit-scrollbar {
  width: 10px; /* 세로 스크롤바 너비 */
  height: 10px; /* 가로 스크롤바 높이 */
}

/* 스크롤바 슬라이더 */
::-webkit-scrollbar-thumb {
  background: #a8a8a8; /* 슬라이더 색상 */
  border-radius: 10px; /* 둥근 모서리 */
}

/* 슬라이더에 마우스를 올렸을 때 */
::-webkit-scrollbar-thumb:hover {
  background: #555; /* 호버 시 색상 */
}


</style>