<template>
  <div class="register">
    <p class="fw-bold mb-4">chatconnect 회원가입</p>
    <p>아이디와 이메일로 간편하게 chatconnect를 시작하세요!</p>
    <div>
      <label for="username">이름</label>
      <input
        id="username"
        v-model="username" 
        placeholder="사용자 이름" 
        required 
      />
    </div>
    <div>
      <label for="id">아이디</label>
      <input
        id="id"
        v-model="id" 
        placeholder="아이디" 
        required 
      />
    </div>
    <div>
      <label for="password">비밀번호</label>
      <input 
        id="pasword"
        type="password" 
        v-model="password" 
        placeholder="비밀번호" 
        required 
      />
    </div>
    <div>
      <label for="email">이메일</label>
      <input
        id="email"
        type="email" 
        v-model="email" 
        placeholder="이메일" 
        required 
      />
    </div>
    <div>
      <label for="phonenumber">전화번호</label>
      <input
        id="phonenumber"
        type="text" 
        v-model="phonenumber" 
        placeholder="전화번호" 
        required 
      />
    </div>
    <div>
      <label for="profileimage">프로필 이미지</label>
      <input
        id="profileimage"
        type="file" 
        @change="onFileChange"
        accept="image/*"
        required 
      />
    </div>
    <button @click="register">회원가입</button>
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
      profileImage: null,
    };
  },
  methods: {
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
        formData.append('profileImage', this.profileImage);

        const response = await axios.post('http://localhost:5000/register', formData);
        console.log('회원가입한 사용자', response.data);

        await this.$store.dispatch('fetchUserData');

        this.$router.push('/');
      } catch (error) {
        console.error(error.response ? error.response.data : error);
      }
    },
    onFileChange(event) {
      // 사용자가 선택한 파일 저장
      const file = event.target.files[0];
      if (file) {
        this.profileImage = file;
      }
    }
  },
};
</script>
