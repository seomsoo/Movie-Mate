<template>
  <div @click="closeSearchBar" class="app-container">
    <header>
      <nav id="navbar" class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid">
          <RouterLink class="navbar-brand" :to="{ name: 'HomePageView' }">
            <img src="@/assets/nav_logo.png" alt="Logo" class="d-inline-block align-text-top">
          </RouterLink>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              
              <li class="nav-item" v-if="movieStore.user">
                <RouterLink class="nav-link fs-4" :to="{ name: 'GenrePageView' }">장르별</RouterLink>
              </li>
              <li class="nav-item" v-if="movieStore.user">
                <RouterLink class="nav-link fs-4" :to="{ name: 'AiRecommendationView' }">AI 추천</RouterLink>
              </li>
              <li class="nav-item" v-if="movieStore.user">
                <RouterLink class="nav-link fs-4" :to="{ name: 'CommunityPageView' }">MovieMates</RouterLink>
              </li>
            </ul>
            <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
              <li class="nav-item" v-if="!movieStore.user">
                <RouterLink class="nav-link fs-4" :to="{ name: 'LoginView'}">로그인</RouterLink>
              </li>
              <li class="nav-item" v-if="!movieStore.user">
                <RouterLink class="nav-link fs-4" :to="{ name: 'SignUpView' }">회원가입</RouterLink>
              </li>
            </ul>
            <ul class="navbar-nav align-items-center">
                <li class="nav-item me-3" v-if="movieStore.user && !showSearchBar">
                  <a href="#" class="nav-link" @click="toggleSearchBar"><i class="fas fa-search fa-lg"></i></a>
                </li>
                <li class="nav-item" v-if="showSearchBar">
                  <form @submit.prevent="searchMovies">
                    <input type="text" v-model="searchQuery" class="form-control search-input" placeholder="제목" @click.stop />
                  </form>
                </li>
              <li class="nav-item dropdown me-4" v-if="movieStore.user">
                <a class="nav-link dropdown-toggle" href="#" id="profileDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  <i class="fas fa-user fa-lg"></i>
                </a>
                <ul class="dropdown-menu dropdown-menu-end dropdown-dark" aria-labelledby="profileDropdown">
                  <li>
                    <RouterLink class="dropdown-item" :to="{ name: 'ProfileView', params: { username: movieStore.user.username } }">마이 페이지</RouterLink>
                  </li>
                  <li>
                    <RouterLink class="dropdown-item" :to="{ name: 'ProfileEditView', params: { username: movieStore.user.username } }">프로필 편집</RouterLink>
                  </li>
                  <li><hr class="dropdown-divider" color="white"></li>
                  <li><a href="#" class="dropdown-item" @click="logout">로그아웃</a></li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
    <div id="background">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView, useRouter, useRoute } from 'vue-router'
import { useMovieStore } from './stores/movie'
import axios from 'axios'
import { onMounted, ref, watch } from 'vue';

const movieStore = useMovieStore()
const route = useRoute()
const router = useRouter()
const showSearchBar = ref(false)
const searchQuery = ref('')
const API_URL = 'http://127.0.0.1:8000'

const toggleSearchBar = (event) => {
  showSearchBar.value = !showSearchBar.value
  event.stopPropagation()
}

const closeSearchBar = () => {
  showSearchBar.value = false
}

const logout = () => {
  console.log(movieStore.token)
  axios({
    method: 'post',
    url: `${API_URL}/api/v1/accounts/logout/`,
    headers: {
      Authorization: `Token ${movieStore.token}`
    }
  })
  .then(() => {
    movieStore.logout()
    router.push({ name: 'HomePageView' })
  })
  .catch((error) => {
    console.log(movieStore.user)
    console.error(error)
  })
}

const getUserData = () => {
  axios({
    method: 'get',
    url: `${API_URL}/api/v1/accounts/user/`,
    headers: {
      Authorization: `Token ${movieStore.token}`
    }
  })
  .then(response => {
    movieStore.user = response.data
  })
  .catch(error => {
    console.error(error)
  })
}
const searchMovies = () => {
  router.push({ name: 'SearchResultView', query: { q: searchQuery.value } });
}


onMounted(getUserData)
</script>

<style scoped>

#navbar {
  background-color: black;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}

.search-input {
  background-color: black !important;
  color: white !important;
  border: 1px solid white;
}

.search-input::placeholder {
  color: rgb(172, 167, 167);
}

.dropdown-dark {
  background-color: black;
  color: white;
}

.dropdown-dark .dropdown-item {
  color: white;
}

.dropdown-dark .dropdown-item:hover {
  background-color: #444;
}

.navbar-brand img {
  width: 90px;
  height: 60px;
  margin-left: 30px;
}

.nav-link {
  font-size: 1.25rem;
}

.fa-lg {
  font-size: 1.5rem;
}

.app-container {
  position: relative;
  overflow-x: hidden;
}
</style>
