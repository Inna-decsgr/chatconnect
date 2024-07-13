<template>
  <div>
    <h2>친구들 목록</h2>
    <ul>
      <li v-for="(user, index) in filteredUsers" :key="index">
        {{ user.username }}
        <button @click="startchat(user)">채팅하기</button>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  computed: {
    ...mapState(['users', 'user']),  // 전체 사용자들을 users에 저장, mapState를 사용하면 store의 users를 가져올수있음
    filteredUsers() {
      return this.users.filter(user => user.username !== this.user.username);
    }
  },
  mounted() {
    // 사용자 목록을 가져오는 액션 호출
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