<template>
  <div class="text-center py-5">
    <div class="text-xl">
      <button class="mb-[20px]" @click="gotoHome">
        <i class="fa-solid fa-user" :class="{'text-gray-400': $route.path !== '/mainchat'}"></i>
      </button><br/>
      <button @click="gotoChattingList">
        <i class="fa-brands fa-rocketchat" :class="{'text-gray-400' : $route.path !== '/chattinglist'}"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    gotoHome() {
      this.$router.push('/mainchat')
    },
    gotoChattingList() {
      this.$router.push('/chattinglist')
    }
  }
}
</script>