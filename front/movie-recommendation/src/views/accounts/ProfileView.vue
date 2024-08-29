<template>
  <div class="profile-container">
    <div class="text-center">
      <img :src="profileImageUrl" alt="Profile Image" class="rounded-circle profile-img">
      <h2>{{ user.username }}</h2>
      <p>{{ user.email }}</p>
      <button class="btn btn-outline-light" @click="goToProfileEdit" v-if="isOwnProfile">
        <i class="bi bi-gear"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useMovieStore } from '@/stores/movie';
import axios from 'axios';

const movieStore = useMovieStore();
const route = useRoute();
const router = useRouter();
const user = ref({});
const likedMovies = ref([]);
const API_URL = 'http://127.0.0.1:8000';
const isOwnProfile = computed(() => user.value.username === movieStore.user.username);
const goDetailPage = (movieId) => {
  router.push(`/${movieId}`)
}


const profileImageUrl = computed(() => {
  return user.value.profile_image ? `${API_URL}${user.value.profile_image}` : 'default-image-path.jpg'; // provide a default image path
});

const getUserData = () => {
  const username = route.params.username;
  axios.get(`${API_URL}/api/v1/accounts/profile/${username}/`, {
    headers: {
      Authorization: `Token ${movieStore.token}`
    }
  })
  .then(response => {
    user.value = response.data;
    getLikedMovies(username); // Use username to fetch liked movies
  })
  .catch(error => {
    console.error(error);
  });
};

const getLikedMovies = (username) => {
  axios.get(`${API_URL}/api/v1/accounts/profile/${username}/`, {
    headers: {
      Authorization: `Token ${movieStore.token}`
    }
  })
  .then(response => {
    likedMovies.value = response.data;
    console.log(likedMovies.value)
  })
  .catch(error => {
    console.error('Failed to fetch liked movies:', error);
  });
};

watch(
  () => movieStore.user,
  (newUser) => {
    if (newUser) {
      getUserData();
    }
  },
  { immediate: true }
);

const goToProfileEdit = () => {
  router.push({ name: 'ProfileEditView', params: { username: user.value.username } });
};

onMounted(() => {
  getUserData();
});
</script>

<style scoped>
.profile-container {
  color: #fff;
}
.profile-img {
  width: 150px;
  height: 150px;
  object-fit: cover;
}
.profile-stats {
  display: flex;
  justify-content: center;
  gap: 10px;
}
.btn-outline-light {
  color: #fff;
  border-color: #fff;
}
.btn-outline-light:hover {
  color: #000;
  background-color: #fff;
  border-color: #fff;
}
.liked-movies-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}
.movie-card {
  width: 100px;
  height: 150px;
  overflow: hidden;
}
.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}
</style>
