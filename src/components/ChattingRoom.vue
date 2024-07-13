<template>
  <p>상대방: {{ friendName }}</p>
  <p>나: {{ user.username }}</p>
</template>

<script>
import { mapState } from 'vuex'
export default {
  computed: {
    ...mapState(['user'])
  },
  props: {
    friendId: {
      type: String,
      required: true
    },
    friendName: {
      type: String,
      required: true
    }
  }
}
</script>