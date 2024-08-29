<template>
  <div class="random-list">
    <div class="header">
      <h2>오늘의 운명을 결정할 랜덤 영화!</h2>
      <button @click="refreshMovies" class="refresh-button btn">
        <i class="fas fa-random"></i>
      </button>
    </div>
    <div v-if="firstMovieYouTubeId" class="youtube-container">
      <iframe
        width="100%"
        height="700"
        :src="`https://www.youtube.com/embed/${firstMovieYouTubeId}?autoplay=1&mute=1`"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      ></iframe>
    </div>
    <div class="slider-container" @mouseover="showButtons" @mouseleave="hideButtons">
      <button class="prev-button" :class="{ 'visible': buttonsVisible }" @click="prevSlide">＜</button>
      <div class="movies-container" ref="slider">
        <RandomListItem
          v-for="r_movie in randomMovies"
          :key="r_movie.id"
          :r_movie="r_movie"
          class="movie-item"
        />
      </div>
      <button class="next-button" :class="{ 'visible': buttonsVisible }" @click="nextSlide">＞</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import RandomListItem from '@/components/movies/RandomListItem.vue'

const API_URL = 'http://127.0.0.1:8000'  // API URL을 설정하세요
const randomMovies = ref([])
const slider = ref(null)
const buttonsVisible = ref(false)
const firstMovieYouTubeId = ref('')

const fetchRandomMovies = () => {
  axios({
    method: 'GET',
    url: `${API_URL}/api/v1/movies/recommend/random`,
  })
  .then(response => {
    randomMovies.value = response.data
    if (randomMovies.value.length > 0) {
      getYouTubeId(randomMovies.value[0].title)
    }
  })
  .catch(error => {
    console.error('Random Movies Error', error)
  })
}

const getYouTubeId = (movieTitle) => {
  axios.get(`https://www.googleapis.com/youtube/v3/search`, {
    params: {
      part: 'snippet',
      q: `${movieTitle} trailer`,
      type: 'video',
      key: 'AIzaSyA-HVd27HuT8mplxf8lXCx-bnhyJ4aG6Z0'
    }
  }).then(response => {
    const data = response.data
    if (data.items && data.items.length > 0) {
      firstMovieYouTubeId.value = data.items[0].id.videoId
    }
  }).catch(error => {
    console.error('Error fetching YouTube video ID:', error)
  })
}

const refreshMovies = () => {
  fetchRandomMovies()
}

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
  fetchRandomMovies()
})
</script>

<style scoped>
.random-list {
  margin: 20px;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 40px;
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

.refresh-button {
  margin-bottom: 5px;
  padding: 8px 16px;
  font-size: 10px;
  border-radius: 5px;
  transition: background-color 0.3s, color 0.3s;
  color: white; /* 아이콘 색상을 흰색으로 설정 */
}

.refresh-button i {
  font-size: 40px; /* 아이콘 크기를 키우기 */
}

.refresh-button:hover {
  color: #91eb38;
}
</style>