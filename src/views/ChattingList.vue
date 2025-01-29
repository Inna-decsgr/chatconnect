<template>
  <div>
    <div class="pt-3 pb-2">
      <p class="text-lg font-bold pl-5 pb-3">채팅 <i class="fa-solid fa-caret-down"></i></p>
      <div>
        <ChatCard :messages="groupedMessages"/>
      </div>
    </div>
  </div>
</template>

<script>
import ChatCard from '../components/ChatCard'
import axios from 'axios';


export default {
  data() {
    return {
      groupedMessages: []
    }
  },
  components: {
    ChatCard
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    }
  },
  mounted() {
    this.getLastMessage();
  },
  methods: {
    async getLastMessage() {
      try {
        const response = await axios.get(`http://localhost:5000/lastmessage/${this.user.userid}`);
        
        this.groupedMessages = Object.values(
          response.data.reduce((acc, message) => {
            const chatId = message.chat_id;

            if (!acc[chatId] || new Date(message.created_at) > new Date(acc[chatId].created_at)) {
              // 상대방 정보를 display_user로 설정
              acc[chatId] = {
                ...message,
                display_user: {
                    id: message.receiver_id,
                    name: message.receiver_name,
                    profile_image: message.profile_image
                  } // 내가 보낸 경우, receiver 정보를 저장
              };
            }
            return acc;
          }, {})
        );
        console.log('채팅방별 최신 메시지:', this.groupedMessages);
      } catch (error) {
        console.error('메세지 가져오기 실패', error.response?.data || error.message);
      }
    },
  }
}
</script>