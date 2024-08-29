<template>
  <div class="article-list">
    <div class="article-row" v-for="(pair, index) in articlePairs" :key="index">
      <ArticleListItem 
        v-for="article in pair" 
        :key="article.pk" 
        :article="article" 
        class="article-column"
      />
    </div>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie'
import ArticleListItem from '@/components/community/ArticleListItem.vue'
import { computed } from 'vue'

const store = useMovieStore()

const articlePairs = computed(() => {
  const pairs = []
  for (let i = 0; i < store.articles.length; i += 2) {
    pairs.push(store.articles.slice(i, i + 2))
  }
  return pairs
})
</script>

<style scoped>
.article-list {
  padding-left: 4rem;
  padding-right: 6rem;
  background-color: transparent;
  border-radius: 10px;
}

.article-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  border-bottom: 1px solid #444444;
  padding-bottom: 1rem;
  margin-top: 1rem;
}

.article-column {
  border-right: 1px solid #444444;
  padding-right: 1rem;
}

.article-column:last-child {
  border-right: none;
  padding-right: 10;
}

.article-row:last-child {
  border-bottom: none;
  margin-bottom: 0;
}
</style>