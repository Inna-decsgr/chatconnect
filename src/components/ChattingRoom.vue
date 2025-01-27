<template >
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
            <p class="text-sm" v-if="msg.sender_id !== user.userid">{{ msg.sender_name }}</p>
            <div class="flex">
              <p class="text-sm" :class="['message', msg.sender_id === user.userid ? 'sender' : 'receiver']">{{ msg.text }}</p>
              <p v-if="!msg.is_read" class="unread-indicator">1</p>
              <p class="time">{{ msg.created_at }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="flex bg-red-100">
    <input 
      type="text" 
      class="basis-5/6 text-xs p-3" 
      v-model="newMessage" 
      placeholder="메시지 입력" 
      @keyup.enter="sendmessage"
    >
    <button class="text-xs basis-1/6" @click="sendmessage">전송</button>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import { v4 as uuidv4 } from 'uuid';
import { formatDatetime } from '@/utils/formatDate';

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
            created_at: formatDatetime(msg.created_at)  
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
            created_at: formatDatetime(response.data.created_at)
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
  position: relative;
}

.receiver-wrapper {
  align-items: flex-start; 
}

.message-container {
  display: flex;
  flex-direction: column;
  max-width: 70%;
  position: relative;
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

.sender-wrapper .time {
  font-size: 12px;
  color: darkgray;
  align-self: flex-start; /*시간을 왼쪽에 정렬*/
  position: absolute;
  top: 50%; /* 말풍선 중앙에 위치 */
  left: -50px; /* 말풍선 왼쪽으로 이동 */
}

/* 읽지 않은 메시지 (1)를 시간 위에 작은 크기로 표시 */
.sender-wrapper .unread-indicator {
  font-size: 10px;
  color: orange;
  font-weight: bold;
  position: absolute;
  top: 25%; /* 시간 위로 이동 */
  left: 0; /* 말풍선 왼쪽으로 이동 */
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
  margin-left: 7px;
  color: darkgray;
  align-self: flex-end; /* 시간을 오른쪽으로 정렬 */
}
</style>