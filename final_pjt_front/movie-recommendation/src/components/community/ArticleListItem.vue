<template>
  <div class="article-item">
    <RouterLink :to="{ name: 'DetailPostView', params: { id: article.pk } }" class="article-title">
      {{ article.title }}
    </RouterLink>
    <p class="article-content">{{ article.content }}</p>
    <div class="article-footer">
      <div class="article-meta">
        <span class="username">{{ article.user.username }}</span>
        <span class="comments">
          <i class="fas fa-comment"></i>
          {{ article.comment_count }}
        </span>
      </div>
      <span class="article-time">{{ formattedCreatedAt }}</span>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { ref, computed } from 'vue'

// 게시물 데이터를 받아옵니다.
const props = defineProps({
  article: {
    type: Object,
    required: true
  }
})

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
const formattedCreatedAt = computed(() => timeAgo(props.article.created_at))
</script>

<style scoped>
.article-item {
  width: calc(50% - 1rem);
  background-color: transparent;
  border-radius: 10px;
  margin-bottom: 1rem;
  padding: 1rem;
  display: inline-block;
  vertical-align: top;
}

.article-title {
  font-size: 1.7rem;
  font-weight: bold;
  color: #ffffff;
  text-decoration: none;
  display: block;
  margin-bottom: 0.5rem;
}

.article-title:hover {
  color: #1db954;
}

.article-content {
  margin-top: 2rem;
  color: #cccccc;
  font-size: 1.3rem;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2rem;
}

.article-meta {
  display: flex;
  align-items: center;
}

.article-meta .username {
  margin-right: 1rem;
  color: #888888;
  font-size: 0.9rem;
}

.article-meta .comments {
  display: flex;
  align-items: center;
  color: #888888;
  font-size: 0.9rem;
}

.article-meta .comments i {
  margin-right: 0.3rem;
}

.article-time {
  color: #888888;
  font-size: 0.9rem;
}

hr {
  border: 0;
  border-top: 1px solid #444444;
  margin: 1rem 0;
}
</style>