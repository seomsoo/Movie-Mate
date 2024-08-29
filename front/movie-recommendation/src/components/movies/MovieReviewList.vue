<template>
  <div class="movie-review-list">
    <h2>사용자 리뷰</h2>
    <ul class="review-list">
      <li v-for="review in reviews" :key="review.pk" class="review-item">
        <div class="review-header">
          <img v-if="review.user.profile_image" :src="`${store.API_URL}${review.user.profile_image}`" alt="profile image" class="profile-image">
          <p><strong>{{ review.user.username }}</strong></p>
        </div>
        <p>한줄 평: {{ review.content }}</p>
        <p>평점: {{ review.rating }} / 5</p>
        <p>작성일: {{ formatDate(review.created_at) }}</p>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, defineExpose } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import { useMovieStore } from '@/stores/movie'

const reviews = ref([])
const route = useRoute()
const store = useMovieStore()
const moviePk = route.params.movieId

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

const fetchReviews = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/${moviePk}/reviews/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then(response => {
      reviews.value = response.data
    })
    .catch(error => {
      console.error('리뷰를 불러오는 데 실패했습니다:', error)
    })
}

fetchReviews()

defineExpose({
  fetchReviews
})
</script>

<style scoped>
.movie-review-list {
  max-width: 800px;
  padding: 20px;
  background-color: transparent;
  color: white;
  border-radius: 8px;
}

.movie-review-list h2 {
  margin-bottom: 20px;
}

.movie-review-list .review-list {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  padding: 0;
  list-style-type: none;
}

.movie-review-list .review-item {
  flex: 0 0 auto;
  padding: 10px;
  margin-right: 20px;
  border-bottom: none;
  border-right: 1px solid #333;
  white-space: nowrap;
}

.movie-review-list .review-header {
  display: flex;
  align-items: center;
}

.movie-review-list .profile-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

.movie-review-list .review-item p {
  margin: 5px 0;
}

.movie-review-list .review-item p strong {
  color: #ccc;
}
</style>