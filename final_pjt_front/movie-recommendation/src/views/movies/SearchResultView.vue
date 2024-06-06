<template>
  <div class="container mt-5">
    <div v-if="movies.length === 0" class="mt-4">검색 결과가 없습니다.</div>
    <div v-else class="row">
      <div v-for="movie in movies" :key="movie.id" class="col-md-3 mb-4">
        <div class="card h-100 movie-card">
          <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" alt="poster" class="card-img-top movie-poster" @click="goDetailPage(movie.pk)">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';
const route = useRoute();
const movies = ref([]);
const router = useRouter();

const goDetailPage = (movieId) => {
  console.log(`/${movieId}`);
  router.push(`/${movieId}`);
};

const fetchMovies = () => {
  const movieName = route.query.q;
  axios.get(`${API_URL}/api/v1/movies/search/${movieName}/`)
    .then(response => {
      movies.value = response.data;
    })
    .catch(error => {
      console.error('영화 검색 오류:', error);
    });
};

onMounted(fetchMovies);

watch(() => route.query.q, fetchMovies);
</script>

<style scoped>
.container {
  margin-top: 100px; /* Navbar와 떨어지게 설정 */
}

.movie-card {
  border: none;
  background-color: transparent; /* 배경 테두리 흰색 투명 제거 */
  transition: transform 0.3s, box-shadow 0.3s;
}

.movie-card:hover {
  transform: scale(1.1); /* 더 웅장하게 보이도록 설정 */
  box-shadow: 0 8px 16px rgba(255, 255, 255, 0.2);
}

.movie-poster {
  cursor: pointer;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
