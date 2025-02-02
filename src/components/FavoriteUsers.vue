<template>
  <div>
    <div>
      <div class="flex items-center justify-between py-[7px]">
        <p class="text-xs text-gray-500 font-bold py-3 px-4">즐겨찾기</p>
        <button v-if="this.favoriteusers.length >= 1" @click="togglefavorite">
          <i :class="showfavorite ? 'fa-chevron-up' : 'fa-chevron-down'" class="fa-solid text-xs text-gray-500 pr-[27px]"></i>
        </button>
      </div>
      <div v-if="showfavorite" class=" mb-7">
        <div v-for="friend in this.favoriteusers" :key="friend.user_id">
          <UserCard :favorites="friend" :favorite="true" :includefriends="favoriteusers"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import UserCard from './UserCard.vue';

export default {
  data() {
    return {
      favoriteusers: [],
      showfavorite: false
    }
  },
  components: {
    UserCard
  },
  watch: {
    '$store.getters.getFavoriteUsers': {
      handler(newValue) {
        console.log('즐겨찾기 목록 변경됨:', newValue);
        this.favoriteusers = newValue || []; // ✅ 기본값 설정
      },
      deep: true
    }
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    },

  },
  mounted() {
    this.getFavoriteUsers();
  },
  methods: {
    async getFavoriteUsers() {
      console.log(this.user.userid);
      const response = await axios.get(`http://localhost:5000/getfavoritelist/${this.user.userid}`)
      console.log('사용자의 즐겨찾기 친구 목록', response.data);
      this.favoriteusers = response.data.map(user => user);
      this.$store.commit('SET_FAVORITE', this.favoriteusers);
      console.log('즐겨찾기된 사용자', this.favoriteusers);
    },
    togglefavorite() {
      this.showfavorite = !this.showfavorite
    }
  }
}
</script>