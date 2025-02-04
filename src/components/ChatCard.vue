<template>
  <div>
    <div v-for="message in messages" :key="message.chat_id" class="flex justify-between items-center px-4 py-[12px] mb-[2px] cursor-pointer hover:bg-gray-100" @dblclick="startchat({id:message.display_user.id, name:message.display_user.name, image:message.display_user.profile_image})">
      <div class="flex items-center">
        <img :src="message.display_user.profile_image ? `http://localhost:5000${message.display_user.profile_image}` : '/images/사용자 프로필.png'" alt="사용자 프로필 이미지" class="w-[50px] h-[50px] object-cover rounded-[20px]">
        <div class="pl-3">
          <p class="font-bold text-sm pb-1">{{ message.display_user.name }}</p>
          <p class="text-xs text-gray-500">{{ message.text }}</p>
        </div>
      </div>
      <div class="text-center">
        <p class="text-xs text-gray-500 pb-1">{{ formattedDate(message.created_at) }}</p>
        <span v-if="user.user_id !== message.sender_id && unreadMessages[message.chat_id]" class="text-xs bg-red-500 text-white block w-[20px] h-[20px] p-[2px] rounded-full font-bold ml-4">{{ unreadMessages[message.chat_id] || null}}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { formatDatetime } from '@/utils/formatDate';
import axios from 'axios';

export default {
  data() {
    return {
      unreadMessages: {}
    }
  },
  props: {
    messages: {
      type: Object,
      required: true
    }
  },
  watch: {
    messages: {
      immediate: true,  // 변경이 없어도 바로 실행. 컴포넌트 로드 시 한번 실행. 이후 messages 가 변경될 때도 자동으로 반응
      handler(newMessages) {
        newMessages.forEach((message) => {
          this.fetchreadcounts(message.chat_id);
        })
      }
    }
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    }
  },
  async mounted() {
    // 메시지들의 chat_id를 fetchreadcounts에 전달해서 데이터 가져오도록 요청 보냄.
    await this.messages.forEach((message) => {
      this.fetchreadcounts(message.chat_id);
    });
  },
  methods: {
    startchat(user) {
      this.$router.push({
        path: '/mainchat/chatroom',
        query: {id: user.id, username: user.name, image:user.image}
      })
    },
    formattedDate(date) {
      return formatDatetime(date)
    },
    async fetchreadcounts(chatid) {
      const response = await axios.get(`http://localhost:5000/messages/${chatid}`);
      // 조건: receiver_id가 나이고 is_read가 0인 메시지 필터링
      const unreadCount = response.data.reduce((count, m) => {
        return m.receiver_id == this.user.userid && !m.is_read ? count + 1 : count;
      }, 0);
      console.log(`채팅방 ${chatid}의 읽지 않은 메세지 개수:`, unreadCount);
      this.unreadMessages[chatid] = unreadCount;
    }
  }
}
</script>