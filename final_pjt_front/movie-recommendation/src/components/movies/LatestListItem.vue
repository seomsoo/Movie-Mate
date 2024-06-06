<template>
  <div class="movie-item">
    <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" alt="" class="movie-poster" @click="goDetailPage(movie.id)">
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

defineProps({
  movie: Object
})

const router = useRouter()
const goDetailPage = (movieId) => {
  console.log(`/${movieId}`);
  router.push(`/${movieId}`);
};
</script>

<style scoped>


.movie-poster {
  cursor: pointer;
  width: 230px; 
  height: auto;
  border-radius: 10px; /* 이미지에 둥근 모서리 추가 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 이미지에 그림자 추가 */
}
</style>
