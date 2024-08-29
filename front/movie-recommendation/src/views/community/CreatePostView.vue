<template>
  <div class="create-post-container">
    <h1>게시글 작성</h1>
    <form @submit.prevent="createArticle">
      <div class="form-group">
        <label for="title"></label>
        <input type="text" v-model.trim="title" id="title" placeholder="제목을 입력하세요.">
      </div>
      <div class="form-group">
        <label for="content"></label>
        <textarea v-model.trim="content" id="content" placeholder="글을 입력하세요."></textarea>
      </div>
      <div class="sub-button">
        <input type="submit" value="글쓰기" class="submit-button">
      </div>
    </form>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useMovieStore } from '@/stores/movie'
import { useRouter } from 'vue-router'

const store = useMovieStore()
const title = ref('')
const content = ref('')
const router = useRouter()

const createArticle = function () {
  axios({
    headers: {
      Authorization: `Token ${store.token}`
    },
    method: 'post',
    url: `${store.API_URL}/api/v1/articles/`,
    data: {
      title: title.value,
      content: content.value
    }
  })
    .then((response) => {
      console.log(response.data)
      router.push({ name: 'CommunityPageView' })
    })
    .catch((error) => {
      console.log(error)
    })
}
</script>

<style scoped>
.create-post-container {
  display: flex;
  flex-direction: column;
  padding: 2rem;
  background-color: rgba(0, 0, 0, 0.8);
  color: #fff;
  border-radius: 10px;
  max-width: 1200px;
  height: 800px;
  margin: 0 auto;
  margin-top: 50px;
}

h1 {
  margin-bottom: 2rem;
  font-size: 2.5rem;
  color: #fff;
}

.form-group {
  width: 100%;
  margin-bottom: 1.5rem;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid #444;
  border-radius: 5px;
  background-color: #222;
  color: #fff;
  font-size: 1rem;
}

textarea {
  height: 500px; /* 콘텐츠 입력 창의 세로 크기 */
}

input[type="text"]:focus,
textarea:focus {
  border-color: #1db954;
  outline: none;
}

input[type="text"]::placeholder,
textarea::placeholder {
  color: #888;
}

.sub-button {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
}

.submit-button {
  padding: 0.75rem 1.5rem;
  background-color: #1db954;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #1ed760;
}
</style>