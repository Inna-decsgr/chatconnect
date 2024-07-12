<template>
  <div>
    <p>친구들과 채팅을 시작해보세요</p>
    <button @click="logout">로그아웃</button>
    <nav>
      <router-link to="/mainchat/chatlist">Chat List</router-link>
      <router-link to="/mainchat/chatroom">Chat Room</router-link>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  methods: {
    logout() {
      this.$store.dispatch('logout');
      this.$router.push('/')
    }
  }
}
</script>