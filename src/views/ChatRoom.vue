<template>
  <ChattingRoom :friend-id="friendId" :friend-name="friendName"/>
</template>

<script>
import { mapState } from 'vuex'
import ChattingRoom from '../components/ChattingRoom.vue'

export default {
  computed: {
    ...mapState(['user']),   // user는 현재 로그인한 사용자
    friendId() {  // friendId는 채팅하기를 클릭해서 채팅할 상대
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