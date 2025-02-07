<template>
  <div class="flex flex-col h-screen bg-white">
    <div class="flex flex-col w-[450px] h-[600px] mx-auto my-auto">
      <p class="text-lg font-bold text-center pb-4">회원가입</p>
      <div>
        <div class="relative w-[100px] h-[100px] mx-auto">
          <img 
            :src="previewImage || (profileImage ? `http://localhost:5000${profileImage}` : '/images/사용자 프로필.png')" 
            alt="프로필 이미지" 
            class="relative mx-auto rounded-3xl w-[80px] h-[80px] object-cover mb-4"
          />

          <button @click="triggerFileInput" class="absolute bottom-[15px] right-[3px] border bg-gray-50 rounded-full flex justify-center items-center w-[25px] h-[25px]">
            <i class="fa-solid fa-camera text-xs"></i>
          </button>
          <input
            ref="fileInput"
            id="profileImage"
            type="file" 
            accept="image/*"
            required
            class="hidden"
            @change="onFileChange"
          />
        </div>
      </div>

      <div>
        <label for="username" class="w-[120px] text-center font-bold text-sm">이름</label>
        <input
          id="username"
          v-model="username" 
          placeholder="사용자 이름" 
          required 
          class="py-2 px-2 w-[280px] rounded-md text-sm border-1 border-gray-300 outline-none mb-2"
        />
      </div>
      <div>
        <label for="id" class="w-[120px] text-center font-bold text-sm">아이디</label>
        <input
          id="id"
          v-model="id" 
          placeholder="아이디" 
          required 
          class="py-2 px-2 w-[280px] rounded-md text-sm border-1 border-gray-300 outline-none mb-2"
        />
      </div>
      <div>
        <label for="password" class="w-[120px] text-center font-bold text-sm">비밀번호</label>
        <input 
          id="pasword"
          type="password" 
          v-model="password" 
          placeholder="비밀번호" 
          required 
          class="py-2 px-2 w-[280px] rounded-md text-sm border-1 border-gray-300 outline-none mb-2"
        />
      </div>
      <div>
        <label for="email" class="w-[120px] text-center font-bold text-sm">이메일</label>
        <input
          id="email"
          type="email" 
          v-model="email" 
          placeholder="이메일" 
          required 
          class="py-2 px-2 w-[280px] rounded-md text-sm border-1 border-gray-300 outline-none mb-2"
        />
      </div>
      <div>
        <label for="phonenumber" class="w-[120px] text-center font-bold text-sm">전화번호</label>
        <input
          id="phonenumber"
          type="text" 
          v-model="phonenumber" 
          placeholder="전화번호" 
          required 
          class="py-2 px-2 w-[280px] rounded-md text-sm border-1 border-gray-300 outline-none mb-2"
        />
      </div>
      <div class="flex mx-auto gap-2 mt-8">
        <button @click="home" class="block w-[200px] bg-gray-100 py-2 px-3 rounded-md hover:bg-gray-200 font-bold text-sm">홈</button>
        <button @click="register" class="block w-[200px] bg-gray-100 py-2 px-3 rounded-md hover:bg-gray-200 font-bold text-sm">회원가입</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      id: '',
      password: '',
      email: '',
      phonenumber: '',
      profileImage: null, // Base64 대신 파일 객체 저장
      previewImage: "/images/사용자 프로필.png", // 미리보기용 기본 이미지
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    onFileChange(event) {
      const file = event.target.files[0];
      console.log('이미지 파일', file);

      if (file) {
        this.profileImage = file; // 파일 객체 저장

        const reader = new FileReader();
        reader.onload = (e) => {
          this.previewImage = e.target.result; // 이미지 미리보기 URL 생성
        };
        reader.readAsDataURL(file);
      }
    },
    async register() {
      try {
        console.log('회원가입 시작!');
        // FormData 생성
        const formData = new FormData();
        formData.append('username', this.username);
        formData.append('id', this.id);
        formData.append('password', this.password);
        formData.append('email', this.email);
        formData.append('phonenumber', this.phonenumber);

        if (this.profileImage) {
          formData.append('profileImage', this.profileImage);
        }

        const response = await axios.post('http://localhost:5000/register', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        console.log('회원가입한 사용자', response.data);

        await this.$store.dispatch('fetchUserData');

        this.$router.push('/');
      } catch (error) {
        console.error(error.response ? error.response.data : error);
      }
    },
    home() {
      this.$router.push('/')
    }
  },
};
</script>
