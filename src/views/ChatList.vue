<template>
  <p v-if="user">나: {{ user.username }}</p>
  
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState(['user'])
  },
  mounted() {
    if (!this.user) {
      this.$store.dispatch('fetchUserData');
    }
  },
}
</script>