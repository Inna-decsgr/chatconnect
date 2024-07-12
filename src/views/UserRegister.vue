<template>
  <div>
    <h2>회원가입</h2>
    <input v-model="username" placeholder="Username" /><br/>
    <input type="password" v-model="password" placeholder="Password" /><br/>
    <button @click="register">회원가입</button>
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
