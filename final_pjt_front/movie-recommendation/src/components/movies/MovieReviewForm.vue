<template>
  <div class="movie-review-form">
    <h2>이 작품에 대한 생각을 자유롭게 표현해보세요.</h2>
    <form @submit.prevent="checkAndSubmitReview">
      <div class="form-group">
        <input type="text" v-model="content" class="form-control" placeholder="이 작품에 대한 생각을 자유롭게 표현해보세요..." required>
      </div>
      <div class="form-group">
        <label for="rating">평점:</label>
        <select v-model="rating" id="rating" class="form-control rating-select" required>
          <option value="" disabled selected hidden>평점을 선택하세요</option>
          <option value="5">★★★★★</option>
          <option value="4">★★★★</option>
          <option value="3">★★★</option>
          <option value="2">★★</option>
          <option value="1">★</option>
        </select>
      </div>
      <button type="submit" class="btn btn-secondary mt-3">글쓰기</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useMovieStore } from '@/stores/movie'
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  moviePk: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['review-submitted'])

const store = useMovieStore()
const content = ref('')
const rating = ref(null)

const fetchReviews = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/${props.moviePk}/reviews/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then(response => {
      // 사용자가 이미 리뷰를 작성했는지 확인
      const userReview = response.data.find(review => review.user.pk === store.user.pk)
      if (userReview) {
        alert('이미 작성한 리뷰가 있습니다!')
      } else {
        submitReview()
      }
    })
    .catch(error => {
      console.error('리뷰를 불러오는 데 실패했습니다:', error)
    })
}

const submitReview = () => {
  const reviewData = {
    content: content.value,
    rating: rating.value,
  }

  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/movies/${props.moviePk}/rating/`,
    data: reviewData,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then(response => {
      console.log('리뷰 제출 성공:', response.data)
      // 리뷰 제출 후 폼 초기화
      content.value = ''
      rating.value = null
      emit('review-submitted')  // 이벤트 발생
    })
    .catch(error => {
      console.error('리뷰 제출 실패:', error)
    })
}

const checkAndSubmitReview = () => {
  fetchReviews()
}
</script>

<style scoped>
.movie-review-form {
  max-width: 800px;
  padding: 20px;
  background-color: transparent;
  color: white;
  border-radius: 8px;
}

.movie-review-form h2 {
  margin-bottom: 20px;
}

.movie-review-form form {
  display: flex;
  flex-direction: column;
}

.movie-review-form .form-group {
  margin-bottom: 15px;
}

.movie-review-form .form-control {
  background-color: rgba(0, 0, 0, 0.8);
  border: none;
  color: white;
  padding: 10px;
  border-radius: 5px;
}

.movie-review-form .form-control::placeholder {
  color: rgba(255, 255, 255, 0.7); /* 흰색으로 변경 */
}

.movie-review-form .rating-select {
  width: auto; /* 선택 칸의 너비를 줄입니다 */
  padding: 5px; /* 선택 칸의 내부 여백을 줄입니다 */
  color: white; /* 선택 칸의 텍스트 색상을 흰색으로 변경 */
}
  
.movie-review-form .rating-select option {
  background-color: rgba(0, 0, 0, 0.8); /* 옵션의 배경색 설정 */
  color: white; /* 옵션의 텍스트 색상을 흰색으로 변경 */
}

.movie-review-form .btn {
  align-self: flex-end;
}
</style>