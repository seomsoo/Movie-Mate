<template>
  <div class="signup-container">
    <h1>회원 가입</h1>
    <form @submit.prevent="signUp">
      <input v-model="username" type="text" placeholder="아이디" required />
      <input v-model="email" type="email" placeholder="이메일 (example@gmail.com)" required />
      <input v-model="password1" type="password" placeholder="비밀번호 (영문, 숫자, 특문 중 2개 조합 10자 이상)" required />
      <input v-model="password2" type="password" placeholder="비밀번호 확인" required />
      <input type="file" @change="onImageSelected" accept="image/*" required />
      <div v-if="imageData">
        <img :src="imageData" alt="Image Preview" class="image-preview" />
      </div>
      <button type="submit">가입하기</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useMovieStore } from '@/stores/movie';

const username = ref('')
const email = ref('')
const password1 = ref('')
const password2 = ref('')
const imageData = ref(null)
const profile_image = ref(null)
const movieStore = useMovieStore()

const onImageSelected = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      imageData.value = e.target.result;
      profile_image.value = file;
    };
    reader.readAsDataURL(file);
  }
};

const signUp = function () {
  const payload = {
    username: username.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value,
    profile_image: profile_image.value
  }
  movieStore.signUp(payload)
}
</script>

<style scoped>
.signup-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  height: 60vh;
  color: #fff; /* 텍스트 색상 */
}

h1 {
  margin-bottom: 20px;
}

form {
  display: flex;
  flex-direction: column;
  width: 300px;
}

input {
  margin-bottom: 10px;
  padding: 10px;

  border-radius: 5px;
  background-color: #000; /* 입력 필드 배경 색상 */
  color: #fff; /* 입력 필드 텍스트 색상 */
}

button {
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #008000; /* 버튼 배경 색상 */
  color: #fff; /* 버튼 텍스트 색상 */
  cursor: pointer;
}

button:hover {
  background-color: #006400; /* 버튼 호버 색상 */
}

.image-preview {
  max-width: 100%;
  height: auto;
  margin-top: 10px;
  border: 1px solid #fff;
  border-radius: 5px;
}
</style>
