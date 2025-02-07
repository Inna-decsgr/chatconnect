<template>
  <div>
    <div :class="{'py-3 px-4': user.userid === me.userid}" class="flex items-center justify-between px-4 py-[7px]">
      <div class="flex items-center">
        <img :src="user.profile_image ? `http://localhost:5000${user.profile_image}` : '/images/사용자 프로필.png'" alt="사용자 프로필 이미지" class="w-[50px] h-[50px] object-cover rounded-[20px]" />
        <div class="pl-3">
          <p class="font-bold text-sm pb-[2px]">{{ user.username }}</p>
          <p class="text-gray-500 text-xs">{{ editedProfileMessage }}</p>
        </div>
      </div>
      <div class="flex items-center">
        <button v-if="user.userid === me.userid" @click="gotoMyProfile">
          <i class="fa-solid fa-gear"></i>
        </button>
        <button v-if="user.userid !== me.userid && !favorite && !isFavorite(this.user.user_id)" @click="setFavorite(user)">
          <i class="fa-regular fa-star"></i>
        </button>
        <button v-if="user.userid !== me.userid && !favorite && isFavorite(this.user.user_id)" @click="removeFavorite(user)">
          <i class="fa-solid fa-star"></i>
        </button>
      </div>
    </div>

    <!--사용자 프로필 수정 팝업-->
    <div v-if="isShowSetting" class="fixed top-[10%] left-1/2 transform -translate-x-1/2 flex flex-col justify-center items-center">
      <div class="w-[400px] h-[500px] bg-white py-5 px-10 rounded-md shadow-lg text-center">
        <div class="flex justify-between items-center w-full mb-5">
          <p class="font-bold">기본프로필 편집</p>
          <button @click="close" class="absolute top-4 right-6">
            <i class="fa-solid fa-x text-xs text-gray-500"></i>
          </button>
        </div>
        <div>
          <div class="relative w-[100px] h-[100px] mx-auto">
            <img 
              :src="previewImage || (user.profile_image ? `http://localhost:5000${user.profile_image}` : '/images/사용자 프로필.png')" 
              alt="프로필 이미지" 
              class="relative w-full h-full object-cover rounded-[38px]" 
            />
            <button @click="triggerFileInput" class="absolute bottom-[-2px] right-[-3px] border bg-gray-50 rounded-full flex justify-center items-center py-[4px] px-[4px]">
              <i class="fa-solid fa-camera"></i>
            </button>
            <input
              ref="fileInput"
              type="file" 
              accept="image/*"
              class="hidden"
              @change="onImageChange"
            />
          </div>
        </div>

        <div class="relative mt-3">
          <input 
            id="username"
            type="text"
            v-model="editedUsername"
            class="w-[300px] border-b border-black p-2 outline-none text-xs"
          />
          <p class="absolute right-[10px] top-1/2 -translate-y-1/2 text-xs text-gray-500 ">{{ editedUsername.length}} / 20</p>
        </div>

        <div class="relative mt-3">
          <input 
            id="profile_message"
            type="text"
            v-model="editedProfileMessage"
            placeholder="상태 메시지"
            class="relative w-[300px] border-b border-black p-2 outline-none text-xs"
          />
          <p class="absolute right-[10px] top-1/2 -translate-y-1/3 text-xs text-gray-500 ">{{ editedProfileMessage.length}} / 60</p>
        </div>

        <div class="userpopup flex justify-end gap-1 mt-5">
          <button :disabled="user.username.trim() === editedUsername.trim()" @click="saveProfile" class="py-2 px-3 rounded-md font-bold text-xs bg-[#f7e330]">
            확인
          </button>
          <button @click="close" class="border py-2 px-3 rounded-md font-bold text-xs hover:bg-gray-50">
            취소
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      isShowSetting: false,
      editedUsername: "", // 수정할 사용자 이름 초기값
      editedProfileMessage: "", // 상태 메시지 초기값
      previewImage: null, // 업로드한 이미지 미리보기
      uploadedImage: null, // 실제 업로드할 이미지 파일
    }
  },
  props: {
    friends: {
      type: Object,
      default: null
    },
    favorites: {
      type: Object,
      default: null
    },
    favorite: {
      type: Boolean,
      default: false
    },
    includefriends: {
      type: Array,
      default: null
    }
  },
  computed: {
    me() {
      return this.$store.getters.getMe;
    },
    user() {
      // getters로 가져온 user도 Vuex 상태(state.user)를 참조하기 때문에 Vuex 상태가 변경되면 이것 또한 반응성 시스템에 의해 자동으로 업데이트된다.
      return this.friends || this.favorites || this.$store.getters.getUser;
    },
    favoriteusers() {
      return this.$store.getters.getFavoriteUsers;
    }
  },
  // Vuex는 Vue의 반응성 시스템을 기반으로 동작, 즉 Vuex상태(state.user)가 변경되면 해당 상태(user)를 사용하는 Vue 컴포넌트가 자동으로 업데이트됨. Vue는 데이터를 참조하고 있는 모든 곳에서 변경을 감지하고, 자동으로 업데이트하도록 설계되어 있음
  // Vuex에서 state를 변경하게 되면 Vue가 이 상태를 사용하는 모든 컴포넌트를 자동으로 업데이트함.
  // Vuex의 mutation은 상태를 변경하기 위한 공식적인 방법이고 상태를 변경하게 되면 Vue의 반응성 시스템이 변경을 감지하고 관련되어 있는 로직을 트리거함. 원래는 명시적으로 commit을 호출해야 실행되지만 vue의 반응성 시스템 덕분에 자동으로 업데이트 됨.
  // watch는 특정 컴포넌트 내에서 특정 데이터의 변화를 감시하고 mutation은 vuex 상태를 변경했을 떄 반응성 시스템을 통해 자동으로 업데이트함
  watch: {
    // watch에서 user를 감시하게 되면 user가 변경될 때 관련 로직(handler)이 자동으로 실행됨
    user: { // this.user가 변경되었을 때 handler 가 실행됨
      immediate: true, // 컴포넌트 생성 시 즉시 감시 시작, mounted 단계, 즉시 handler 실행, 기본적으로 watch는 데이터가 변경될 때만 실행되는데 이 옵션을 통해 초기 실행을 강제함
      handler(newUser) { // user가 변경되었을 때 실행되는 로직, newUser는 변경된 user의 새로운 값, Vue는 user의 값이 변경될 때마다 최신 값을 handler에 전달함
        this.editedUsername = newUser.username || ""; // username이 없으면 빈 값
        this.editedProfileMessage = newUser.profile_message || ""; // profile_message가 없으면 빈 값
      },
    },
  },
  methods: {
    gotoMyProfile() {
      this.isShowSetting = true;
      console.log(this.isShowSetting);
    },
    close() {
      this.isShowSetting = false;
    },
    triggerFileInput() {
      this.$refs.fileInput.click(); // 숨겨진 파일 입력 요소 클릭
    },
    onImageChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.uploadedImage = file; // 업로드할 파일 저장
        const reader = new FileReader();
        reader.onload = (e) => {
          this.previewImage = e.target.result; // 이미지 미리보기 URL 생성
        };
        reader.readAsDataURL(file);
      }
    },
    async saveProfile() {
      // 수정된 데이터를 서버로 전송
      const formData = new FormData();
      formData.append("username", this.editedUsername);
      formData.append("profile_message", this.editedProfileMessage);
      if (this.uploadedImage) {
        formData.append("profile_image", this.uploadedImage);
      }

      console.log("FormData 확인:", formData.get("profile_image")); // 파일 데이터 확인

      const response = await axios.post(`http://localhost:5000/updateprofile/${this.user.userid}`, formData);

      // 업데이트 된 데이터를 다시 가져와서 vuex 상태 업데이트하기
      this.$store.dispatch('fetchUserData');
      
      this.isShowSetting = false;
      console.log(response.data);
    },
    async setFavorite(friend) {
      const response = await axios.post(`http://localhost:5000/addfavorite/${this.me.userid}`, {
        friendid: friend.user_id
      });
      this.$store.commit('addFavoriteUser', friend)
      console.log('친구 즐겨찾기 하기', response.data);
    },
    isFavorite(userId) {
      return (
        this.favoriteusers &&
        this.favoriteusers.some(user => user.user_id === userId)
      );
    },
    async removeFavorite(friend) {
      const response = await axios.post(`http://localhost:5000/removefavorite/${this.me.userid}`, {
        friendid: friend.user_id
      });
      this.$store.commit('removeFavoriteUser', friend.user_id)
      console.log('즐겨찾기 해제', response.data);
    }
  }
}
</script>

<style>
.userpopup button:disabled {
  background-color: #e5e5e5; /* 비활성화된 배경 */
  cursor: not-allowed; /* 비활성화된 커서 */
  color: #999; /* 흐린 텍스트 */
}
</style>