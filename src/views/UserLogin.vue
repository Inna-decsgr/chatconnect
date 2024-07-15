<template>
  <div class="login">
    <h2 class="fw-bold mb-4">로그인</h2>
    <input v-model="username" placeholder="Username" class="form-control form-control-lg mb-3" required @keydown.enter="login"/>
    <input type="password" v-model="password" placeholder="Password"  class="form-control form-control-lg" required @keydown.enter="login"/><br/>
    <button class="btn btn-primary w-100" @click="login">로그인</button>
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
        alert('로그인 성공')
        console.log(response);
        this.$router.push('/mainchat/chatlist');
      } catch (error) {
        console.error(error);
        alert('로그인에 실패하였습니다. 아이디와 비밀번호를 확인해주세요.');
      }
    },
  },
};
</script>

<style>
.login {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -70%);
}
</style>