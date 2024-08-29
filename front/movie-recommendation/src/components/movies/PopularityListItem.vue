<template>
  <div >
    <img :src="'https://image.tmdb.org/t/p/w500' + p_movie.poster_path" alt="" class="movie-poster" @click="goDetailPage(p_movie.id)">
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

defineProps({
  p_movie: Object
})

const router = useRouter()
const goDetailPage = (movieId) => {
  router.push(`/${movieId}`);
};
</script>

<style scoped>
.movie-poster {
  cursor: pointer;
  width: 230px;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>