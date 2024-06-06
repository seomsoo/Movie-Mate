<template>
  <div v-if="movie.id" class="detail-container">
    <div class="movie-poster-container">
      <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" alt="poster" class="movie-poster">
    </div>
    <div class="movie-info-container">
      <h2>{{ movie.title }}</h2>
      <p class="movie-overview">{{ movie.overview || "줄거리 정보가 없습니다." }}</p>
      <p>평점: {{ movie.vote_average ? movie.vote_average.toFixed(1) : "N/A" }}</p>
      <p>개봉일: {{ movie.release_date || "N/A" }}</p>
      <p>상영 시간: {{ movie.runtime ? `${movie.runtime}분` : "N/A" }}</p>
      <p>출연 배우:
        <div class="actors-list">
          <span v-for="actor in movie.actors || []" :key="actor.name">
            {{ actor.name }}
          </span>
        </div>
      </p>
      <p>장르:
        <div class="genres-list">
          <span v-for="genre in movie.genres || []" :key="genre.name">
            {{ genre.name }}
          </span>
        </div>
      </p>
      
      <button type="button" class="btn btn-danger trailer-button" data-bs-toggle="modal" data-bs-target="#movieModal">
        <i class="bi bi-play-circle"></i> 미리 보기
      </button>

      <MovieTrailer v-if="trailer" :movie="movie" :trailer="trailer" />
      <MovieReviewForm :moviePk="movie.id" @review-submitted="onReviewSubmitted" />
      <MovieReviewList ref="reviewList" :moviePk="movie.id" />
    </div>

    <!-- Modal -->
    <div class="modal fade" id="movieModal" tabindex="-1" aria-labelledby="movieModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="movieModalLabel">{{ movie.title }} - 트레일러</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <iframe
              v-if="trailer"
              :src="`https://www.youtube.com/embed/${trailer}`"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
              class="trailer-iframe"
              style="background-color: transparent;"
            ></iframe>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import axios from 'axios'
import MovieTrailer from '@/components/movies/MovieTrailer.vue'
import MovieReviewForm from '@/components/movies/MovieReviewForm.vue'
import MovieReviewList from '@/components/movies/MovieReviewList.vue'

const movieStore = useMovieStore()
const route = useRoute()
const movieId = route.params.movieId
const YOUTUBE_KEY = 'AIzaSyA-HVd27HuT8mplxf8lXCx-bnhyJ4aG6Z0'

const movie = ref({})
const trailer = ref('')

axios({
  method: 'GET',
  url: `${movieStore.API_URL}/api/v1/movies/${movieId}/`,
  headers: {
    Authorization: `Token ${movieStore.token}`
  }
})
.then(response => {
  movie.value = response.data
  return axios({
    method: 'get',
    url: 'https://www.googleapis.com/youtube/v3/search',
    params: { part: 'snippet', key: YOUTUBE_KEY, type: "video", q: movie.value.title }
  })
})
.then((response) => {
  trailer.value = response.data.items[0].id.videoId
  console.log(trailer.value)
})
.catch(error => {
  console.error('Movie Detail Fetch Error:', error)
})

const reviewList = ref(null)

const onReviewSubmitted = () => {
  if (reviewList.value) {
    reviewList.value.fetchReviews()
  }
}
</script>

<style scoped>
.detail-container {
  display: flex;
  color: white;
  background-color: rgba(0, 0, 0, 0.8);
  border-radius: 10px;
  padding: 20px;
}

.movie-poster-container {
  flex: 1;
  margin-right: 20px;
}

.movie-poster {
  width: 100%;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.movie-info-container {
  flex: 2;
  display: flex;
  flex-direction: column;
}

.movie-info-container h2 {
  margin-bottom: 20px;
}

.movie-info-container p {
  margin-bottom: 10px;
}

.actors-list, .genres-list {
  display: flex;
  flex-wrap: wrap;
}

.actors-list span, .genres-list span {
  margin-right: 10px;
}

.trailer-button {
  display: flex;
  align-items: center;
  margin-top: 20px;
  background-color: transparent;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.trailer-button:hover {
  background-color: #28a745;
}

.trailer-button i {
  margin-right: 10px;
  font-size: 2rem;
}

.trailer-iframe {
  background-color: transparent;
  width: 100%;
  height: 315px;
}
</style>
