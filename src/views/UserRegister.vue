<template>
  <div class="register">
    <h2 class="fw-bold mb-4">회원가입</h2>
    <input v-model="username" placeholder="Username" class="form-control form-control-lg mb-3" required @keydown.enter="register"/>
    <input type="password" v-model="password" placeholder="Password" class="form-control form-control-lg" required @keydown.enter="register"/><br/>
    <button class="btn btn-primary w-100" @click="register">회원가입</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('http://localhost:5000/register', {
          username: this.username,
          password: this.password,
        });
        alert(response.data.msg);

        await this.$store.dispatch('login', {
          username: this.username,
          password: this.password,
        });

        await this.$store.dispatch('fetchUserData');

        this.$router.push('/mainchat/chatlist');
      } catch (error) {
        console.error(error.response ? error.response.data : error);
        alert('회원가입 실패');
      }
    },
  },
};
</script>

<style>
.register {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -70%);
}
</style>