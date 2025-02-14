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
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
    unreadmessageslength() {
      return this.$store.getters.getunreadmessages[this.user?.userid] || 0;
    }
  },
  created() {
    this.setupSocketListeners();  // 소켓 이벤트 설정
    this.unreadmessages();  // 초기 unread messages 가져오기
  },
  watch: {
    // 로그인 직후 user가 변경되면 unreadmessages 다시 호출
    user: {
      handler(newUser) {
        if (newUser && newUser.userid) {
          this.unreadmessages();
          this.setupSocketListeners();  // 로그인 후에도 소켓 이벤트 다시 등록
        }
      },
      immediate: true // user가 처음 로드될 때도 실행되도록 설정!
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
    },
    setupSocketListeners() {
      // 소켓 이벤트 설정 관리
      // 서버의 setisreadtrue 라우트에서 emit("get_unread_message", result)를 하게 되면 socket.on("get_unread_message")이 실행됨. 
      if (!this.user || !this.user.userid) return;

      socket.off("get_unread_message");  // 기존 이벤트 리스너 제거(중복 방지)
      socket.on("get_unread_message", (data) => {
        console.log("실시간 업데이트된 읽지 않은 메시지들:", data);

        if (data.userid !== this.user.userid) return;  // 현재 로그인한 사용자만 반영
        
        this.$store.commit("set_unread_messages", {
          userid: data.userid,
          count: data.unread_count
        });
      })
    }
  }
}
</script>