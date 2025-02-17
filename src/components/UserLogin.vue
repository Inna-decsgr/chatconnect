<template>
  <div>
    <div class="flex flex-col items-center mx-auto my-auto">
      <div class="pb-2 w-[300px]">
        <input 
          id="id"
          v-model="id" 
          placeholder="아이디"
          class="py-2 px-2 w-full rounded-md text-sm border-1 border-gray-300 outline-none"
        />
      </div>
      <div class="mb-3 w-[300px]">
        <input 
          id="password"
          type="password"
          v-model="password" 
          placeholder="비밀번호"
          class="py-2 px-2 w-full rounded-md text-sm border-1 border-gray-300 outline-none"
          @keyup.enter="login"
        />
      </div>

      <div class="w-full mx-auto">
        <button @click="login" class="block w-full bg-gray-100 py-2 px-3 rounded-md hover:bg-gray-200 font-bold text-sm border-b">로그인</button>
        <p class="text-xs pt-5 pb-2 text-gray-600">아직 회원이 아니신가요?</p>
        <button @click="gotoregister" class="block w-full bg-gray-100 py-2 px-3 rounded-md hover:bg-gray-200 font-bold text-sm">회원가입</button>
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
        const response = await this.$store.dispatch('login', userdata);
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
