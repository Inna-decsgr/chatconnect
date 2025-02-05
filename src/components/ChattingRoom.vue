<template>
  <div id="app">
    <div>
      <ChatTopBar />
    </div>
    <div class="chat-container p-3" ref="chatContainer">
      <div v-for="(msg, index) in messages" :key="index" class="message-wrapper" :class="msg.sender_id === user.userid ? 'sender-wrapper' : 'receiver-wrapper'">
      <!--쉽게 생각하면 receiver_id, 수신자가 7이고 보내는 사람이 8이라고 치자. 그럼 sender_id와 user.userid는
      8로 같을수밖에 없잖아. 현재 로그인된 사용자가 메시지를 보낼테니까. 근데 우리가 채팅방을 만들때 같은 방을 
      공유하게 만들어뒀으니까 7이 sender가 될수도 receiver가 될수도 있고 8이 sender가 될수도 receiver가 될 수도 있잖아 그치?
      데이터베이스 보면서 이해하면 더 잘될거야. receiver_id가 userid와 같은것만 따로 모아서 왼쪽 정렬하고
      receiver_id와 userid가 다른것만 모아서 오른쪽 정렬하는거야! 그냥 야매로 생각하자면 현재 로그인된
      사용자가 sender가 되어서 오른쪽에 보여야하는거잖아. 그러니까 반대로 생각해서 receiver_id와 userid
      가 같은 것만 골라서 왼쪽정렬하면 v-else했을때 반대의 경우가 다 오른쪽 정렬되니까 그런거라고 생각해.
      미래의 나야...과거의 내가 멍청해서 미안 허허허 내가 고쳤어! 현재 사용자와 sender_id가 
      같지 않으면 수신자라는 거니까 msg.receiver_id === user.userid에서 아래와 같이 바꿈!ㅎㅎ-->
        <div class="message-container">
          <div class="flex">
            <img v-if="msg.sender_id !== user.userid" :src="msg.receiver_profile_image ? `http://localhost:5000${msg.receiver_profile_image}` : '/images/사용자 프로필.png'" class="w-[40px] h-[40px] object-cover rounded-[16px]">
            <div class="pl-3">
              <p class="text-[12px] mb-[6px]" v-if="msg.sender_id !== user.userid">{{ msg.sender_name }}</p>
              <div class="flex">
                <p :class="['message', msg.sender_id === user.userid ? 'sender' : 'receiver']">{{ msg.text }}</p>
                <p v-if="msg.sender_id == user.userid && !msg.is_read" class="unread-indicator">1</p>
                <p class="time">{{ msg.created_at }}</p>
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
import axios from 'axios'
import { mapState } from 'vuex'
import { v4 as uuidv4 } from 'uuid';
import { chatformatTime } from '@/utils/chatformatTime';
import ChatTopBar from './ChatTopBar.vue';

export default {
  components: {
    ChatTopBar
  },
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
  mounted() {
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
    },
    friendImage: {
      type: String,
      required: false
    }
  },
  methods: {
    async loadUserandMessages() {
      await this.$store.dispatch('fetchUserData'); 

      if (this.user && this.user.userid) {
        this.chatId = this.getChatId();
        this.loadMessages();
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
    async loadMessages() {
      try {
        const response = await axios.get(`http://localhost:5000/messages/${this.chatId}`);
        this.messages = response.data.map(msg => {
          return {
            ...msg,
            created_at: chatformatTime(msg.created_at)  
          };
        });
      } catch (error) {
        console.error('메시지 로드 실패:', error)
      }
    },
    async sendmessage() {
      if (this.newMessage.trim()) {
        const timestamp = new Date().toISOString();  
        const messages = {
          chat_id: this.chatId,
          sender_id: this.user.userid,
          sender_name: this.user.username,
          receiver_id: this.friendId,
          receiver_name: this.friendName,
          text: this.newMessage,
          timestamp
        };
        console.log('메세지 정보', messages);

        try {
          const response = await axios.post('http://localhost:5000/messages', messages);
          console.log('보낸 메시지', response.data);
          const formattedMessage = {  
            ...response.data,
            created_at: chatformatTime(response.data.created_at)
          }
          this.messages.push(formattedMessage);
          this.newMessage = '';
          this.$nextTick(() => this.scrollToBottom()) 
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
    },
    async setIsReadTrue(chatid) {
      try {
        // this.chatId랑 this.userid
        //  {{ this.chatId }}{{ this.user.userid }}
        const response = await axios.post(`http://localhost:5000/setisreadtrue/${chatid}`, {
          userid: this.user.userid
        });
        console.log('is_read를 true로', response.data);
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

.message-wrapper {
  display: flex;
  flex-direction: column;
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
  align-items: flex-start;  /* 메세지 왼쪽 정렬*/ 
}

.message-container {
  display: flex;
  flex-direction: row;
  align-items: flex-end;  /* 시간이랑 말풍선 수직 정렬 */
  max-width: 70%;
  margin-bottom: 10px;
}

.sender {
  background-color: #f7e330; 
  border-radius: 4px;
  padding-top: 6px;
  padding-bottom: 6px;
  padding-left: 10px;
  padding-right: 10px;
  margin-left: 55px;
  font-size: 12px;
}


.receiver {
  background-color: white;
  border-radius: 4px;
  padding-top: 6px;
  padding-bottom: 6px;
  padding-left: 10px;
  padding-right: 10px;
  position: relative;
  margin-right: 7px; 
  font-size: 12px;
}

.message-wrapper .time {
  align-content: flex-end;
}

.receiver-wrapper .time {
  color: #555555;
  flex-shrink: 0;
  font-size: 11px;
}
.sender-wrapper .time {
  position: absolute;
  color: #555555;
  flex-shrink: 0;
  align-self: flex-end;
  font-size: 11px;
}


/* 읽지 않은 메시지 (1)를 시간 위에 작은 크기로 표시 */
.sender-wrapper .unread-indicator {
  font-size: 11px;
  color: #f7e330;
  position: absolute;
  margin-left: 40px;
}

.sender::after,
.receiver::after {
  content: '';
  position: absolute;
  width: 0;
  height: 0;
}

.sender::after {
  border-left: 13px solid #f7e330;
  border-top: 2px solid transparent;
  border-bottom: 10px solid transparent;
  right: -10px; 
  top: 8px;
}

.receiver::after {
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