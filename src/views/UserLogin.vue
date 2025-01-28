<template>
  <div>
    <p>로그인</p>
    <div>
      <label for="id">아이디</label>
      <input 
        id="id"
        v-model="id" 
        placeholder="아이디" 
      />
    </div>
    <div>
      <label for="password">비밀번호</label>
      <input 
        id="password"
        v-model="password" 
        placeholder="비밀번호" 
      />
    </div>
    <button @click="login">로그인</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      id: '',
      password: '',
    };
  },
  methods: {
    async login() {
      try {
        const userdata = { id: this.id, password: this.password };
        console.log('로그인할 사용자', userdata);
        const response = await this.$store.dispatch('login', userdata);
        alert('로그인 성공')
        console.log(response);
        this.$router.push('/mainchat');
      } catch (error) {
        console.error(error);
        alert('로그인에 실패하였습니다. 아이디와 비밀번호를 확인해주세요.');
      }
    },
  },
};
</script>
