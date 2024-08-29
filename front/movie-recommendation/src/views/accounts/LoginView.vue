<template>
  <div class='container'>
    <div class="login-container">
      <h1>로그인</h1>
      <form @submit.prevent="logIn">
        <input v-model="username" type="text" placeholder="아이디" required />
        <input v-model="password" type="password" placeholder="비밀번호" required />
        <button type="submit">로그인</button>
      </form>
    </div>
  </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useMovieStore } from '@/stores/movie'; 
  
  const username = ref('');
  const password = ref('');
  const router = useRouter();
  const movieStore = useMovieStore();
  
  const logIn = function () {
    const payload = {
      username: username.value,
      password: password.value
    }
    movieStore.logIn(payload)
  }
  </script>
  
  <style scoped>
  .container {
    background-image: url('@/assets/accounts.png');
    background-size: cover; /* 이미지 크기를 컨테이너에 맞춤 */
    background-position: center; /* 이미지 위치를 중앙으로 */
  }
  .login-container {
    
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 80vh;
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
    margin-bottom: 15px;
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
  </style> 