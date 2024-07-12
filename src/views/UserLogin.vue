<template>
  <div>
    <h2>로그인</h2>
    <input v-model="username" placeholder="Username" /><br/>
    <input type="password" v-model="password" placeholder="Password" /><br/>
    <button @click="login">로그인</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async login() {
      try {
        const credentials = { username: this.username, password: this.password };
        const response = await this.$store.dispatch('login', credentials);
        alert('로그인 성공! Access Token: ' + response.access_token || response.token);
        this.$router.push('/mainchat/chatroom');
      } catch (error) {
        console.error(error);
        alert('로그인에 실패하였습니다.');
      }
    },
  },
};
</script>
