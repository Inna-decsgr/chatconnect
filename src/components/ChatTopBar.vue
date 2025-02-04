<template>
  <div class="bg-[#bad0e5] p-3">
    <div class="flex items-center">
      <img :src="image ? `http://localhost:5000${image}` : '/images/사용자 프로필.png'" alt="사용자 프로필 이미지" class="w-[50px] h-[50px] object-cover rounded-[20px]">
      <div class="pl-3">
        <p class="pb-1">{{ username }}</p>
        <div class="text-gray-500 flex">
          <i class="fa-solid fa-user text-xs"></i>
          <span class="text-xs pl-1">2</span>
        </div>
      </div>
    </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      id: null,
      username: null,
      image: null
    }
  },
  created() {
    this.id = this.$route.query.id;
    this.username = this.$route.query.username;
    this.image = this.$route.query.image;
  }
}
</script>