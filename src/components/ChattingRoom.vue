<template>
  <div v-for="(msg, index) in messages" :key="index" class="message" :class="{ 'my-message': msg.sender_id === user.userid, 'friend-message': msg.receiver_id === user.userid }">
    <!--메시지의 발신자가 현재 로그인된 사용자와 같으면 my-message를 메시지의 -->
    <p v-if="msg.receiver_id === user.userid" style="text-align: left;">
      <strong>{{ msg.sender_name }}:</strong>
      <span>{{ msg.text }}</span>
      <span>{{ msg.created_at }}</span>
    </p>
    <p v-else  style="text-align: right;">
      <strong>{{ msg.sender_name }}</strong>
      <span>{{ msg.text }}</span>
      <span>{{ msg.created_at }}</span>
    </p>
  </div>
  <input type="text" v-model="newMessage" placeholder="메시지 입력">
  <button @click="sendmessage">전송</button>
  <p>{{ this.user }}</p>
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
      chatId: null,
    }
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
  mounted() {
    this.loadUserandMessages();  
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
        this.messages = response.data;
      } catch (error) {
        console.error('메시지 로드 실패:', error)
      }
    },
    async sendmessage() {
      console.log(this.user.userid);
      console.log(this.friendId);
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
          this.messages.push(response.data);
          this.newMessage = '';
        } catch (error) {
          console.error('메시지 전송 실패:', error);
          alert("메시지 전송에 실패했습니다.");
        }
      } else {
        alert('메시지를 입력하세요')
      }
    }
  }
}
</script>

