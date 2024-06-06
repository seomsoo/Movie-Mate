<template>
  <div class="detail-container" v-if="article">
    <div class="article-header">
      <h1>{{ article.title }}</h1>
      <div class="article-info">
        <span class="username">{{ article.user.username }}</span>
        <span class="created-at">{{ formattedCreatedAt }}</span>
        <span class="comments-count">
          <i class="fas fa-comment"></i> {{ comments.length }}
        </span>
        <router-link :to="{ name: 'EditPostView', params: { id: article.pk } }">
          <button class="edit-button">
            <i class="fas fa-edit"></i>
          </button>
        </router-link>
      </div>
    </div>
    <div class="article-content">
      <p class="content">{{ article.content }}</p>
    </div>
    <div class="comments-section">
      <div class="comment-form-wrapper">
        <PostCommentForm v-if="article" :articleId="article.pk" @commentAdded="fetchComments" />
      
      </div>
      <ul v-if="comments.length > 0">
        <li v-for="comment in comments" :key="comment.pk" class="comment-item">
          <img v-if="comment.user.profile_image" :src="`${store.API_URL}${comment.user.profile_image}`" alt="profile image" class="profile-image">
          <div class="comment-content">
            <span class="comment-username">{{ comment.user.username }}</span>
            <span class="comment-date">{{ timeAgo(comment.created_at) }}</span>
            <p>{{ comment.content }}</p>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, computed } from 'vue'
import { useRoute, onBeforeRouteLeave } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import PostCommentForm from '@/components/community/PostCommentForm.vue'

const store = useMovieStore()
const route = useRoute()
const article = ref(null)
const comments = ref([])

const currentUser = computed(() => store.user)

const fetchComments = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/comments/`
  })
    .then((response) => {
      comments.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
}

const fetchArticle = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/`
  })
    .then((response) => {
      article.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
}

// 시간을 포맷하는 함수를 정의합니다.
function timeAgo(date) {
  const now = new Date();
  const past = new Date(date);
  const seconds = Math.floor((now - past) / 1000);
  let interval = Math.floor(seconds / 31536000);

  if (interval >= 1) {
    return `${interval}년 전`;
  }
  interval = Math.floor(seconds / 2592000);
  if (interval >= 1) {
    return `${interval}달 전`;
  }
  interval = Math.floor(seconds / 86400);
  if (interval >= 1) {
    return `${interval}일 전`;
  }
  interval = Math.floor(seconds / 3600);
  if (interval >= 1) {
    return `${interval}시간 전`;
  }
  interval = Math.floor(seconds / 60);
  if (interval >= 1) {
    return `${interval}분 전`;
  }
  return "방금 전";
}

// 게시물 생성 시간을 포맷하여 표시합니다.
const formattedCreatedAt = computed(() => timeAgo(article.value?.created_at))

onMounted(() => {
  fetchArticle()
  fetchComments()
})

onBeforeRouteLeave((to, from, next) => {
  if (to.name === 'EditPostView' && article.value && currentUser.value && article.value.user.username !== currentUser.value.username) {
    alert('수정 권한이 없습니다.')
    next(false)
  } else {
    next()
  }
})
</script>

<style scoped>
.content{
  margin-bottom: 3rem;
}
.detail-container {
  max-width: 1200px;
  max-height: 2000px;
  height: 800px;
  margin: 0 auto;
  padding: 2rem;
  background-color: rgba(0, 0, 0, 0.8);
  color: #fff;
  border-radius: 10px;
  margin-top: 50px;
}

.article-header {
  margin-bottom: 1.5rem;
}

.article-info {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  color: #888;
  margin-top: 1rem;
}

.article-info span {
  margin-right: 0.5rem;
}

.username {
  margin-right: 1rem;
}

.created-at {
  margin-right: 1rem;
}

.comments-count {
  margin-right: auto;
}

.edit-button-wrapper {
  margin-left: auto;
}

.edit-button {
  background: none;
  border: none;
  color: #1db954;
  cursor: pointer;
  font-size: 3rem; /* 아이콘 크기 */
  margin-left: 920px;
}

.edit-button:hover {
  color: #1ed760;
}


.comments-section {
  border-top: 1px solid #444;
  padding-top: 1rem;
}


.comment-form-wrapper textarea {
  flex-grow: 1;
  padding: 0.5rem;
  background: none;
  border: 1px solid #444;
  border-radius: 5px;
  color: #fff;
}

.comment-form-wrapper textarea:focus {
  border-color: #1db954;
  outline: none;
}


.comment-item {
  display: flex;
  margin-bottom: 1rem;
  margin-right: 3rem;
  padding-right: 2rem;
}

.profile-image {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 1rem;
  margin-top: 0.5rem;
}

.comment-content {
  border-radius: 5px;
  padding: 0.5rem;
  flex-grow: 1;
}

.comment-username {
  font-weight: bold;
  margin-right: 0.5rem;
}

.comment-date {
  font-size: 0.8rem;
  color: #888;
}

.comment-content p {
  margin: 0.5rem 0 0 0;
  
}
</style>