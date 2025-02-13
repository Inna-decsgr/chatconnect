<template>
  <div class="text-center py-5">
    <div class="text-xl">
      <button class="mb-[20px]" @click="gotoHome">
        <i class="fa-solid fa-user" :class="{'text-gray-400': $route.path !== '/mainchat'}"></i>
      </button><br/>
      <button @click="gotoChattingList" class="relative">
        <i class="fa-brands fa-rocketchat" :class="{'text-gray-400' : $route.path !== '/chattinglist'}"></i>
        <span v-if="unreadmessageslength > 0" class="text-xs bg-red-500 text-white block w-[18px] h-[18px] rounded-full font-bold absolute top-[-5px] left-3 pt-[1px] text-center">{{ unreadmessageslength }}</span>
      </button>
    </div>
  </div>
</template>

<script>
import socket from "../utils/socket";


export default {
  data() {
    return {
      unreadmessageslength: null
    }
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    }
  },
  created() {
    if (this.user && this.user.userid) {
      // 읽지 않은 메시지 개수 업데이트 이벤트 수신
      socket.on("get_unread_message", (messages) => {
        console.log("실시간 업데이트된 읽지 않은 메시지들:", messages);
        this.unreadmessageslength = messages.length
      })
    }

    this.unreadmessages();
  },
  watch: {
    // user가 바뀌면 unreadmessages 다시 호출
    user: {
      handler(newUser) {
        if (newUser && newUser.userid) {
          this.unreadmessages();
        }
      },
      deep: true,  // user 내부의 값이 변해도 감지
    }
  },
  methods: {
    gotoHome() {
      this.$router.push('/mainchat')
    },
    gotoChattingList() {
      this.$router.push('/chattinglist')
    },
    async unreadmessages() {
      if (!this.user || !this.user.userid) return;
      console.log('socket.emit getunreadmessage 실행');
      socket.emit("get_unread_message", { user_id: this.user.userid });
    }
  }
}
</script>