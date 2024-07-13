<template>
  <div>
    <h2>로그인</h2>
    <input v-model="username" placeholder="Username" required @keydown.enter="login"/><br/>
    <input type="password" v-model="password" placeholder="Password" required @keydown.enter="login"/><br/>
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
        this.$router.push('/mainchat/chatlist');
      } catch (error) {
        console.error(error);
        alert('로그인에 실패하였습니다. 아이디와 비밀번호를 확인해주세요.');
      }
    },
  },
};
</script>
