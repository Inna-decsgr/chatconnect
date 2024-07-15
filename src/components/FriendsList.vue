<template>
  <div class="mt-4">
    <p class="fs-6 text-secondary">👥 친구 {{ filteredUsers.length }}</p>
    <ul class="d-flex flex-column">
      <li v-for="(user, index) in filteredUsers" :key="index" class="d-flex justify-content-between align-items-center w-100 mb-3">
        <span class="fs-5">{{ user.username }}</span>
        <button class="btn btn-primary" @click="startchat(user)">채팅하기</button>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  computed: {
    ...mapState(['users', 'user']),   
    filteredUsers() {
      return this.users.filter(user => user.username !== this.user.username);
    }
  },
  mounted() {
    this.$store.dispatch('getFriends')
  },
  methods: {
    startchat(user) {
      this.$router.push({
        path: '/mainchat/chatroom',
        query: {id: user.user_id, username: user.username}
      })
    }
  }
}
</script>