<template>
  <FriendsList />
</template>

<script>
import { mapState } from 'vuex'
import FriendsList from '../components/FriendsList.vue'

export default {
  computed: {
    ...mapState(['user'])
  },
  mounted() {
    if (!this.user) {
      this.$store.dispatch('fetchUserData');
    }
  },
  components: {
    FriendsList
  }
}
</script>