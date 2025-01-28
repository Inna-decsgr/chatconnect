<template>
  <div class="flex h-screen">
    <div v-if="user" class="w-[70px] bg-gray-100 border-r">
      <MainBar />
    </div>
    <div class="flex-1">
      <router-view />
    </div>
  </div>
</template>

<script>
import MainBar from './components/MainBar.vue'

export default {
  components: {
    MainBar
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    }
  }
}
</script>




<style>
.app-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.content-wrapper {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%); 
    width: 100%; 
    height: 100%;
    max-width: 700px;
    max-height: 1000px;
    border: 1px solid #dee2e6; 
    border-radius: 8px;
    background-color: white; 
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    box-sizing: border-box;
}

ol, ul {
  list-style: none;
  padding: 0 !important;  
  margin: 0;       
}
</style>
