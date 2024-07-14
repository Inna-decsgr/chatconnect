<template>
  <div v-if="user" class="p-2">
    <div class="justify-content-between align-items-center mb-4">
      <p class="fs-4 fw-bold">친구들과 채팅을 시작해보세요</p>
      <button class="btn btn-primary w-50" @click="logout">로그아웃</button>
    </div>
    <p v-if="user" class="fs-5 border-bottom pb-4">나 : {{ user.username }}</p>
    <nav class="fs-5 mt-3">
      <router-link to="/mainchat/chatlist">친구 목록</router-link>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
import { mapState } from 'vuex';
export default {
  computed: {
    ...mapState(['user']),
  },
  methods: {
    logout() {
      this.$store.dispatch('logout');
      this.$router.push('/')
    }
  }
}
</script>


<style>
.router-link {
  color: gray; 
}
.router-link-active {
  font-weight: bold;
}
</style>