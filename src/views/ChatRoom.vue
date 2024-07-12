<template>
  <ChattingRoom />
</template>

<script>
import { mapState } from 'vuex'
import ChattingRoom from '../components/ChattingRoom.vue'

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
    ChattingRoom
  }
}
</script>