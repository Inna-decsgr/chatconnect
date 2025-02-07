<template>
  <div class="flex flex-col absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-[60%] text-center">
    <img src="/images/chatlog.png" alt="챗커넥트 로고" class="w-[300px] mx-auto">
    <div class="mt-4">
      <UserLogin />
    </div>
  </div>
</template>

<script>
import UserLogin from '../components/UserLogin.vue'

export default {
  components: {
    UserLogin
  },
}
</script>
