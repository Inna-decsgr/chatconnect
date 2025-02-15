<template>
  <div>
    <div v-for="message in messages" :key="message.chat_id" class="flex justify-between items-center px-4 py-[12px] mb-[2px] cursor-pointer hover:bg-gray-100" @dblclick="startchat({id:message.display_user.id, name:message.display_user.name, image:message.display_user.profile_image})">
      <div class="flex items-center">
        <img :src="message.display_user.profile_image ? `http://localhost:5000${message.display_user.profile_image}` : '/images/사용자 프로필.png'" alt="사용자 프로필 이미지" class="w-[50px] h-[50px] object-cover rounded-[20px]">
        <div class="pl-3">
          <p class="font-bold text-sm pb-1">{{ message.display_user.name }}</p>
          <p class="text-xs text-gray-500">
            {{ newText[message.chat_id] ? newText[message.chat_id] : message.text }}
          </p>
        </div>
      </div>
      <div class="pb-3">
        <p class="text-xs text-gray-500 pb-1">
          {{ newTime[message.chat_id] ? formattedDate(newTime[message.chat_id]) : formattedDate(message.created_at) }}
        </p>
        <span v-if="user.user_id !== message.sender_id && unreadMessages[message.chat_id]" class="text-xs bg-red-500 text-white block w-[18px] h-[18px] rounded-full font-bold absolute right-[26px] pt-[1px] text-center">{{ unreadMessages[message.chat_id] || null}}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { formatDatetime } from '@/utils/formatDate';
import socket from "../utils/socket";
import axios from 'axios';

export default {
  data() {
    return {
      unreadMessages: {},
      newText: [],
      newTime: []
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
      handler(newMessages) {
        if (!newMessages || newMessages.length === 0) {
          console.log("messages가 비어 있음! 데이터를 기다려야 함!");
          return;
        }
        for (const message of newMessages) {
          this.fetchunreadcounts(message.chat_id);
        }
      },
      immediate: true,  // 컴포넌트가 처음 로드될 때도 실행
      deep: true        // messages 내부 값이 변경될 때도 감지
    }
  },  
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
    unreadMessagesSafe() {
      return this.unreadMessages || {};  // undefined일 경우 기본값 `{}` 반환
    }
  },
  async mounted() {
    for (const message of this.messages) {  // `for...of`는 `await`를 정상적으로 지원
      await this.fetchunreadcounts(message.chat_id);  // 비동기 함수 실행
    }
    this.fetchreadcounts();
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
    fetchreadcounts() {
      socket.off("update_unread_by_chat"); 
      socket.on("update_unread_by_chat", (data) => {
        // 데이터가 현재 로그인한 사용자 데이터인지 확인
        console.log('받은 전체 데이터', data)
        if (data.userid == this.user.userid) {
          this.unreadMessages = { ...this.unreadMessagesSafe, ...data.unread_by_chat };
          this.newText[data.chatid] = data.text;
          this.newTime[data.chatid] = data.created_at;
        } else {
          console.log("🚫 [Socket] 내 데이터가 아니므로 무시됨");
        }
      });
    },
    async fetchunreadcounts(chatid) {
      const response = await axios.get(`http://localhost:5000/messages/${chatid}`);

      // 조건: receiver_id가 나이고 is_read가 0인 메시지 필터링
      const unreadCount = response.data.reduce((count, m) => {
        return m.receiver_id == this.user.userid && !m.is_read ? count + 1 : count;
      }, 0);
      this.unreadMessages[chatid] = unreadCount;
    }
  }
}
</script>