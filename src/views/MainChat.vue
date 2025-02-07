<template>
  <div v-if="user">
    <div class="h-screen bg-white">
      <div>
        <div class="flex items-center justify-between pt-3 pb-2">
          <p class="text-lg font-bold pl-5">친구</p>
          <div class="pr-4">
            <button class="border py-1 px-2 rounded-md text-xs" @click="logout">로그아웃</button>
          </div>
        </div>
        <div class="pb-2 border-b">
          <UserCard />
        </div>
        <div class="border-b">
          <FavoriteUsers />
        </div>
        <div>
          <FriendsList />
        </div>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import UserCard from '../components/UserCard.vue'
import FriendsList from '../components/FriendsList.vue'
import FavoriteUsers from '../components/FavoriteUsers.vue'

export default {
  components: {
    UserCard,
    FriendsList,
    FavoriteUsers
  },
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

body {
  overflow: hidden;
}
</style>