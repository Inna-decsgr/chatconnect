<template>
  <div>
    <button @click="gotoregister">회원가입</button>
    <button @click="gotologin">로그인</button>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
export default {
  setup() {
    const router = useRouter();

    return {router}
  },
  methods: {
    gotoregister() {
      this.router.push('/register');
    },
    gotologin() {
      this.router.push('/login');
    }
  }
}
</script>