<template>
  <div class="profile-edit-container container mt-5" v-if="profile">
    <h2>프로필 수정</h2>
    <form @submit.prevent="updateProfile">
      <div class="mb-3">
        <label for="avatar" class="form-label">프로필 이미지</label>
        <input type="file" class="form-control" id="avatar" @change="onFileChange">
      </div>
      <div class="mb-3">
        <label for="username" class="form-label">사용자 이름</label>
        <input type="text" class="form-control" id="username" v-model="profile.username" readonly>
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">이메일</label>
        <input type="email" class="form-control" id="email" v-model="profile.email">
      </div>
      <div class="mb-3">
        <label for="old_password" class="form-label">현재 비밀번호</label>
        <input type="password" class="form-control" id="old_password" v-model="profile.old_password">
      </div>
      <div class="mb-3">
        <label for="new_password1" class="form-label">새 비밀번호</label>
        <input type="password" class="form-control" id="new_password1" v-model="profile.new_password1">
      </div>
      <div class="mb-3">
        <label for="new_password2" class="form-label">새 비밀번호 확인</label>
        <input type="password" class="form-control" id="new_password2" v-model="profile.new_password2">
      </div>
      <div class="text-center">
        <button type="submit" class="btn btn-outline-light">저장</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';
import { useMovieStore } from '@/stores/movie';

const movieStore = useMovieStore();

const router = useRouter();
const route = useRoute();
let selectedFile = null;

const profile = ref(null);

const fetchUserProfile = () => {
  const username = route.params.username;
  axios.get(`${movieStore.API_URL}/api/v1/accounts/profile/${username}`, {
    headers: {
      Authorization: `Token ${movieStore.token}`
    }
  })
  .then((response) => {
    profile.value = {
      username: response.data.username,
      email: response.data.email,
      old_password: '',
      new_password1: '',
      new_password2: ''
    };
  })
  .catch((error) => {
    console.error('사용자 정보를 불러오지 못했습니다.', error);
  });
};

const onFileChange = (e) => {
  selectedFile = e.target.files[0];
};

const updateProfile = () => {
  const formData = new FormData();
  formData.append('username', profile.value.username);
  formData.append('email', profile.value.email);
  formData.append('old_password', profile.value.old_password);
  formData.append('new_password1', profile.value.new_password1);
  formData.append('new_password2', profile.value.new_password2);
  if (selectedFile) {
    formData.append('profile_image', selectedFile);
  }

  const username = route.params.username;
  axios({
    method: 'PUT',
    url: `${movieStore.API_URL}/api/v1/accounts/profile/${username}/`,
    data: formData,
    headers: {
      Authorization: `Token ${movieStore.token}`,
      'Content-Type': 'multipart/form-data'
    }
  })
  .then((response) => {
    const updatedUsername = response.data.username;
    console.log(updatedUsername);
    router.push({ name: 'HomePageView', params: { username: updatedUsername } });
  })
  .catch((error) => {
    console.error('프로필 수정에 실패했습니다.', error);
  });
};

onMounted(() => {
  fetchUserProfile();
});
</script>

<style scoped>
.profile-edit-container {
  color: #fff;
}

.form-control {
  background-color: transparent;
  color: #fff;
  border: 1px solid #fff;
}

.form-control::placeholder {
  color: #fff;
}

.btn-outline-light {
  color: #fff;
  border-color: #fff;
  background-color: green;
}

.btn-outline-light:hover {
  color: #000;
  background-color: #fff;
  border-color: #fff;
}

.text-center {
  text-align: center;
}
</style>
