<template>
  <div class="community-container">
    <div class="title">
      <h1>씨네마 파트너 찾기</h1>
      <RouterLink :to="{ name: 'CreatePostView' }" class="write-button">
        글쓰기
      </RouterLink>
    </div>
    <ArticleList />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useMovieStore } from '@/stores/movie';
import { RouterLink } from 'vue-router'
import ArticleList from '@/components/community/ArticleList.vue'

const store = useMovieStore()
onMounted(() => {
  store.getArticles()
})
</script>

<style scoped>
.community-container {
  padding: 2rem;
  background-color: rgba(0, 0, 0, 0.8);
  border-radius: 10px;
}

.title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: aliceblue;
  margin-bottom: 1rem;
}

h1 {
  padding-left: 50px;
  font-size: 45px;
}

.write-button {
  margin-right: 50px;
  padding: 0.6rem 1.2rem;
  background-color: #3c8154;
  color: #fff;
  text-decoration: none;
  border-radius: 5px;
}

.write-button:hover {
  background-color: #288134;
}
</style>