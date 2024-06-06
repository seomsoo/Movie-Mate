<template>
  <div class="top-rated-list">
    <h4>압도적인 평점을 받은 명작</h4>
    <div class="slider-container" @mouseover="showButtons" @mouseleave="hideButtons">
      <button class="prev-button" :class="{ 'visible': buttonsVisible }" @click="prevSlide">＜</button>
      <div class="movies-container" ref="slider">
        <TopRatedListItem
          v-for="t_movie in movieStore.topRatedMovies"
          :key="t_movie.id"
          :t_movie="t_movie"
          class="movie-item"
        />
      </div>
      <button class="next-button" :class="{ 'visible': buttonsVisible }" @click="nextSlide">＞</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMovieStore } from '@/stores/movie'
import TopRatedListItem from '@/components/movies/TopRatedListItem.vue'

const movieStore = useMovieStore()
const slider = ref(null)
const buttonsVisible = ref(false)

const nextSlide = () => {
  if (slider.value) {
    const maxScrollLeft = slider.value.scrollWidth - slider.value.clientWidth
    if (slider.value.scrollLeft >= maxScrollLeft) {
      slider.value.scrollLeft = 0
    } else {
      slider.value.scrollLeft += slider.value.clientWidth
    }
  }
}

const prevSlide = () => {
  if (slider.value) {
    if (slider.value.scrollLeft <= 0) {
      slider.value.scrollLeft = slider.value.scrollWidth - slider.value.clientWidth
    } else {
      slider.value.scrollLeft -= slider.value.clientWidth
    }
  }
}

const showButtons = () => {
  buttonsVisible.value = true
}

const hideButtons = () => {
  buttonsVisible.value = false
}

onMounted(() => {
  movieStore.fetchTopRatedMovies()
})
</script>

<style scoped>
.top-rated-list {
  margin: 20px;
}

.slider-container {
  display: flex;
  align-items: center;
  position: relative;
  border-radius: 15px;
  overflow: hidden;
}

.movies-container {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  scroll-behavior: smooth;
  flex-grow: 1;
  border-radius: 15px;
  scrollbar-width: none; /* Firefox */
  padding: 0 10px; /* 슬라이드 컨테이너의 패딩을 추가하여 간격 조정 */
}

.movies-container::-webkit-scrollbar {
  display: none; /* Safari and Chrome */
}

.movies-container:hover::-webkit-scrollbar {
  display: block; /* Show scrollbar on hover */
  height: 8px;
}

.movies-container::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 10px;
}

.movies-container:hover::-webkit-scrollbar-thumb {
  background-color: #555;
}

.movie-item {
  flex: 0 0 auto;
  margin: 0 10px; 
}

.prev-button,
.next-button {
  background-color: transparent;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 10px;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  transition: opacity 0.3s;
  opacity: 0;
}

.prev-button {
  left: 10px;
}

.next-button {
  right: 10px;
}

.prev-button:hover,
.next-button:hover {
  color: rgba(95, 243, 87, 0.879); 
}

.prev-button.visible,
.next-button.visible {
  opacity: 1;
}
</style>
