<template>
  <div class="flex h-screen">
    <div class="w-[450px] h-[600px] mx-auto my-auto">
      <p class="text-lg font-bold text-center pb-4">로그인</p>
      <div class="pb-2">
        <label for="id" class="w-[100px] text-center font-bold">아이디</label>
        <input 
          id="id"
          v-model="id" 
          placeholder="아이디"
          class="py-2 px-2 w-[280px] rounded-md text-sm border-1 border-gray-300 outline-none"
        />
      </div>
      <div class="pb-[50px]">
        <label for="password" class="w-[100px] text-center font-bold">비밀번호</label>
        <input 
          id="password"
          v-model="password" 
          placeholder="비밀번호"
          class="py-2 px-2 w-[280px] rounded-md text-sm border-1 border-gray-300 outline-none"
        />
      </div>

      <div class="w-[350px] mx-auto">
        <button @click="login" class="block w-[350px] bg-gray-100 py-2 px-3 rounded-md hover:bg-gray-200 font-bold text-sm">로그인</button>
        <p class="text-sm pt-3 pb-2 text-gray-600">아직 회원이 아니신가요?</p>
        <button @click="gotoregister" class="block w-[350px] bg-gray-100 py-2 px-3 rounded-md hover:bg-gray-200 font-bold text-sm">회원가입</button>
      </div>
    </div>
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
    gotoregister() {
      this.$router.push('/register');
    },
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
