<template >
  <div class="chat-container mt-4" ref="chatContainer">
    <div v-for="(msg, index) in messages" :key="index" class="message-wrapper" :class="msg.sender_id === user.userid ? 'sender-wrapper' : 'receiver-wrapper'">
      <div class="message-container">
        <p class="fw-bold" v-if="msg.sender_id !== user.userid">{{ msg.sender_name }}</p>
        <p :class="['message', msg.sender_id === user.userid ? 'sender' : 'receiver']">{{ msg.text }}</p>
        <p class="time">{{ msg.created_at }}</p>
      </div>
    </div>
  </div>
  <div class="input-group mt-2">
    <input type="text" class="form-control form-control-lg" v-model="newMessage" placeholder="메시지 입력" @keyup.enter="sendmessage">
    <button class="btn btn-primary" @click="sendmessage">전송</button>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import { v4 as uuidv4 } from 'uuid';

export default {
  data() {
    return {
      newMessage: '',
      messages: [],
      chatId: null
    }
  },
  created() {
    this.loadUserandMessages();  
  },
  updated() {
    this.scrollToBottom();
  },
  computed: {
    ...mapState(['user'])
  },
  props: {
    friendId: {
      type: String,
      required: true
    },
    friendName: {
      type: String,
      required: true
    }
  },
  methods: {
    async loadUserandMessages() {
      await this.$store.dispatch('fetchUserData');  // 사용자 정보 로드하는 액션 호출

      // 사용자 정보가 로드된 후에 getChatId와 loadMessages() 호출
      // 사용자 정보 로드안하고 바로 getChatId 해버리면 user 정보가 없어서 getChatId 함수 ids에 userid가 들어가지 않아서 에러 남!
      if (this.user && this.user.userid) {
        this.chatId = this.getChatId();
        this.loadMessages();
      } else {
        console.error('User is not defined or userid is missing');
      }
    },
    getChatId() {
      const ids = [this.user.userid, this.friendId].sort();// 두 ID를 정렬하여 항상 같은 순서를 유지
      const chatKey = `chatId_${ids.join('_')}`;  // 정렬된 ID를 사용하여 chatKey 생성
      let chatId = localStorage.getItem(chatKey); 

      if (!chatId) {  // 만약 처음 대화를 거는 상대 id가 9인? 라서 로컬스토리지에 chatId가 없다면
        chatId = uuidv4();   // uuid 라이브러리를 사용해서 새로운 chatId를 생성한 다음

        // 로컬스토리지 chatid_9 key에 새로 생성된 chatId를 저장하고 나중에 다시 friendId가 9인 친구에게 채팅을 걸때 이 chatId를 가져와서 메세지 보낼 때 사용된다.
        localStorage.setItem(chatKey, chatId); 
      }
      return chatId;
    },
    async loadMessages() {
      try {
        const response = await axios.get(`http://localhost:5000/messages/${this.chatId}`);
        this.messages = response.data.map(msg => {
          return {
            ...msg,
            created_at: this.formatDatetime(msg.created_at)  // 메세지 가져올 때 시간에 포맷 적용해서 가져오기
          };
        });
      } catch (error) {
        console.error('메시지 로드 실패:', error)
      }
    },
    formatDatetime(datetime) {  // 시간 포맷에 맞게 변환
      const date = new Date(datetime);
      const options = { hour: 'numeric', minute: 'numeric', hour12: true };
      return date.toLocaleString('ko-KR', options);
    },
    async sendmessage() {
      if (this.newMessage.trim()) {
        const timestamp = new Date().toISOString();  // 현재 시간을 ISO 형식으로
        const messages = {
          chat_id: this.chatId,
          sender_id: this.user.userid,
          sender_name: this.user.username,
          receiver_id: this.friendId,
          receiver_name: this.friendName,
          text: this.newMessage,
          timestamp
        };

        try {
          const response = await axios.post('http://localhost:5000/messages', messages);
          const formattedMessage = {  // 메세지가 보내고 나서 받은 응답에서도 created_at에 포맷팅이 적용되도록 수정! 이거 안해주면 처음에 실시간으로 보내진 메세지의 시간을 포맷팅이 되지 않고 새로고침을 눌러야지만 로드된 시간이 보여지기 때문에 보내자마자 바로 포맷팅 시간 보고 싶으면 받은 응답에도 처리해주기!
            ...response.data,
            created_at: this.formatDatetime(response.data.created_at)
          }
          this.messages.push(formattedMessage);
          this.newMessage = '';
          this.$nextTick(() => this.scrollToBottom())  // 메시지 보낸 후에 스크롤 맨 아래로 이동
        } catch (error) {
          console.error('메시지 전송 실패:', error);
          alert("메시지 전송에 실패했습니다.");
        }
      } else {
        alert('메시지를 입력하세요')
      }
    },
    scrollToBottom() {
      const container = this.$refs.chatContainer;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    }
  }
}
</script>

<style>
.chat-container {
  height: 500px;
  overflow-y: auto;
  background: rgb(242, 244, 252);
  padding: 10px;
}

.message-wrapper {
  display: flex;
  flex-direction: column;
}

.sender-wrapper {
  align-items: flex-end; 
}

.receiver-wrapper {
  align-items: flex-start; 
}

.message-container {
  display: flex;
  flex-direction: column;
  max-width: 70%;
}

.message {
  padding: 10px;
  border-radius: 10px;
  margin: 5px 0;
  position: relative;
}

.sender {
  background-color: #e1ffc7; 
  align-self: flex-end; 
}

.receiver {
  background-color: #d1e7ff; 
  align-self: flex-start; 
}

.sender::after,
.receiver::after {
  content: '';
  position: absolute;
  width: 0;
  height: 0;
}

.sender::after {
  border-left: 10px solid #e1ffc7;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
  right: -10px; 
  top: 10px;
}

.receiver::after {
  border-right: 10px solid #d1e7ff;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
  left: -10px;
  top: 10px;
}

.time {
  font-size: 12px;
  color: darkgray;
  align-self: flex-end; /* 시간을 오른쪽으로 정렬 */
}
</style>