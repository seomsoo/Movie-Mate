<template>
  <div class="container py-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div class="d-flex align-items-center">
        <div class="dropdown me-5">
          <button class="btn custom-dropdown" type="button" id="genreDropdown" data-bs-toggle="dropdown" aria-expanded="false">
            {{ selectedGenreName }}
            <i class="bi bi-chevron-down"></i>
          </button>
          <ul class="dropdown-menu" aria-labelledby="genreDropdown">
            <li v-for="genre in genres" :key="genre.id">
              <a class="dropdown-item" @click="selectGenre(genre.id, genre.name)">{{ genre.name }}</a>
            </li>
          </ul>
        </div>
        <div class="dropdown">
          <button class="btn custom-dropdown" type="button" id="sortDropdown" data-bs-toggle="dropdown" aria-expanded="false">
            {{ selectedSortName }}
            <i class="bi bi-chevron-down"></i>
          </button>
          <ul class="dropdown-menu" aria-labelledby="sortDropdown">
            <li><a class="dropdown-item" @click="selectSort('vote-average', '평점순')">평점순</a></li>
            <li><a class="dropdown-item" @click="selectSort('popularity', '인기순')">인기순</a></li>
            <li><a class="dropdown-item" @click="selectSort('vote-count', '추천순')">추천순</a></li>
            <li><a class="dropdown-item" @click="selectSort('latest', '개봉일순')">개봉일순</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div v-if="genreDetail">
      <div class="row row-cols-2 row-cols-md-4 g-4">
        <div v-for="movie in genreDetail.movies" :key="movie.id" class="col">
          <div class="card h-100 bg-transparent text-white border-0">
            <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" class="card-img-top movie-poster" @click="goDetailPage(movie.id)">
            <div class="card-body"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const genres = ref([])
const selectedGenre = ref('')
const selectedGenreName = ref('장르')
const selectedSort = ref('vote-average')
const selectedSortName = ref('평점순')
const genreDetail = ref(null)
const router = useRouter()

const goDetailPage = (movieId) => {
  router.push(`/${movieId}`)
}

const fetchGenres = () => {
  axios.get('http://127.0.0.1:8000/api/v1/movies/genres/')
    .then(response => {
      genres.value = response.data
      if (genres.value.length > 0) {
        selectedGenre.value = genres.value[0].id
        selectedGenreName.value = genres.value[0].name
        fetchGenreDetail()
      }
    })
    .catch(error => {
      console.error(error)
    })
}

const fetchGenreDetail = () => {
  if (selectedGenre.value && selectedSort.value) {
    axios.get(`http://127.0.0.1:8000/api/v1/movies/genre/${selectedGenre.value}/${selectedSort.value}/`)
      .then(response => {
        genreDetail.value = response.data
      })
      .catch(error => {
        console.error('Error fetching genre detail:', error)
      })
  }
}

const selectGenre = (genreId, genreName) => {
  selectedGenre.value = genreId
  selectedGenreName.value = genreName
  fetchGenreDetail()
}

const selectSort = (sortCriteria, sortName) => {
  selectedSort.value = sortCriteria
  selectedSortName.value = sortName
  fetchGenreDetail()
}

onMounted(fetchGenres)
</script>

<style scoped>
@import 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.5.0/font/bootstrap-icons.min.css';

.container {
  background-color: transparent;
}

.dropdown-menu {
  background-color: #2a2a2a;
}


.dropdown-item {
  color: #ece6e6;
  cursor: pointer;
  
}

.dropdown-item:hover {
  background-color: #28a745;
  color: #fff;
}

.movie-poster {
  cursor: pointer;
  border-radius: 10px;
}

.card {
  transition: transform 0.3s ease-in-out;
}

.card:hover {
  transform: scale(1.12 );
}

.custom-dropdown {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  padding: 0;
  color: white;
  
}

.custom-dropdown:hover {
  color: #28a745;
  
}

.custom-dropdown .bi-chevron-down {
  font-size: 2.5rem;
  margin-left: 0.5rem;
}

#genreDropdown {
  font-size: 3rem;
}

#sortDropdown {
  font-size: 2rem;
}

.custom-dropdown:active,
.custom-dropdown:focus,
.custom-dropdown[aria-expanded="true"] {
  background-color: transparent;
  color: #28a745;
}
</style>