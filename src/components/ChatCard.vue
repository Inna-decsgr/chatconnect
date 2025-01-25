<template>
  <div>
    <div v-for="message in messages" :key="message.chat_id" class="flex justify-between items-center px-4 py-[12px] mb-[2px] cursor-pointer hover:bg-gray-100" @dblclick="startchat({id:message.display_user.id, name:message.display_user.name})">
      <div class="flex items-center">
        <img :src="message.display_user.profile_image ? `http://localhost:5000${message.display_user.profile_image}` : '/images/사용자 프로필.png'" alt="사용자 프로필 이미지" class="w-[50px] h-[50px] object-cover rounded-[20px]">
        {{ message}}
        <div class="pl-3">
          <p class="font-bold text-sm pb-1">{{ message.display_user.name }}</p>
          <p class="text-xs text-gray-500">{{ message.text }}</p>
        </div>
      </div>
      <div class="text-center">
        <p class="text-xs text-gray-500 pb-1">{{ formattedDate(message.created_at) }}</p>
        <p class="text-xs text-gray-500">3</p>
      </div>
    </div>
  </div>
</template>

<script>
import { formatDatetime } from '@/utils/formatDate';

export default {
  props: {
    messages: {
      type: Object,
      required: true
    }
  },
  methods: {
    startchat(user) {
      this.$router.push({
        path: '/mainchat/chatroom',
        query: {id: user.id, username: user.name}
      })
    },
    formattedDate(date) {
      return formatDatetime(date)
    },
  }
}
</script>