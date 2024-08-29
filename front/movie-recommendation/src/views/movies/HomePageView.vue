<template>
  <div class="home-container">
    
    <RandomList />
    <br>
    <PopularityList />
    <br>
    <TopRatedList />
    <br>
    <LatestList />
    

  </div>
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
import { onMounted } from 'vue'
import { useMovieStore } from '@/stores/movie'
import TopRatedList from '@/components/movies/TopRatedList.vue'
import LatestList from '@/components/movies/LatestList.vue'
import PopularityList from '@/components/movies/PopularityList.vue'
import RandomList from '@/components/movies/RandomList.vue'
// const movieStore = useMovieStore()
// onMounted(() => {
//   movieStore.fetchNowRunningMovies();
//   movieStore.fetchTopRatedMovies();
// })
</script>

<style scoped>

.home-container {
  padding-top: 10px;
  /* background-color: #000;  */
  color: #fff; 
  
}


p {
  font-size: 18px;
}
</style>
