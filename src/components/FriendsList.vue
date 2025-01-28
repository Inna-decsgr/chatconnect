<template>
  <div>
    <p class="text-xs text-gray-500 font-bold py-3 px-4">친구 {{ filteredUsers.length }}</p>
    <ul class="d-flex flex-column">
      <li v-for="(user, index) in filteredUsers" :key="index" class="d-flex justify-content-between align-items-center w-100 hover:bg-gray-100" @dblclick="startchat(user)">
        <UserCard :friends="user" />
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import UserCard from '../components/UserCard.vue'

export default {
  components: {
    UserCard
  },
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