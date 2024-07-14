<template>
  <div class="home text-center">
    <p class="fw-bold fs-1">ChattConnect</p>
    <p class="fs-6">소소한 일상을 공유해요!</p>
    <div class="btn-group w-100" role="group">
      <button type="button" class="btn btn-primary fw-bold" @click="gotoregister">회원가입</button>
      <button type="button" class="btn btn-primary fw-bold" @click="gotologin">로그인</button>
    </div>
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

<style>
.home {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>