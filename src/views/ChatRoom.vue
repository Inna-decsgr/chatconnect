<template>
  <ChattingRoom :friend-id="friendId" :friend-name="friendName"/>
</template>

<script>
import { mapState } from 'vuex'
import ChattingRoom from '../components/ChattingRoom.vue'

export default {
  computed: {
    ...mapState(['user']),   
    friendId() {  
      return this.$route.query.id
    },
    friendName() {
      return this.$route.query.username
    }
  },
  mounted() {
    if (!this.user) {
      this.$store.dispatch('fetchUserData');
    }
  },
  components: {
    ChattingRoom
  }
}
</script>