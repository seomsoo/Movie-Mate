<template>
  <div class="comment-form-wrapper">
    <form @submit.prevent="submitComment" class="comment-form">
      <div class="form-group">
        <label for="content"></label>
        <textarea v-model="content" id="content" placeholder="댓글을 입력하세요." @keydown.enter="submitComment">
        </textarea>
      </div>
      <button type="submit" class="submit-button">글쓰기</button>
    </form>
  </div>
</template>

<script setup>
import { ref, defineEmits, defineProps } from 'vue'
import axios from 'axios'
import { useMovieStore } from '@/stores/movie'

const emit = defineEmits(['commentAdded'])

const { articleId } = defineProps({
  articleId: Number
})

const store = useMovieStore()
const content = ref('')

const submitComment = function () {
  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/articles/${articleId}/comments/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
    data: {
      content: content.value
    }
  })
    .then((response) => {
      console.log(response.data)
      content.value = '' // 댓글 작성 후 내용 초기화
      emit('commentAdded') // 부모 컴포넌트에 이벤트 발생
    })
    .catch((error) => {
      console.error(error.response.data) // 오류 응답 데이터 출력
    })
}
</script>

<style scoped>
.comment-form-wrapper {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.comment-form {
  display: flex;
  align-items: center;
  width: 100%;
}

.form-group {
  flex-grow: 1;
}

textarea {
  width: 100%;
  height: 50px; /* 댓글 입력 창 높이 */
  padding: 0.5rem;
  background: none;
  border: 1px solid #444;
  border-radius: 5px;
  color: #fff;
  resize: none;
}

textarea:focus {
  border-color: #1db954;
  outline: none;
}

textarea::placeholder {
  color: #888;
}

.submit-button {
  margin-left: 1rem;
  padding: 0.75rem 1.5rem;
  background-color: #1db954;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  margin-bottom: 6px;
}

.submit-button:hover {
  background-color: #1ed760;
}
</style>