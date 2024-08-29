import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useRouter } from 'vue-router';

export const useMovieStore = defineStore('movie', () => {
  const user = ref(null);
  const token = ref(null); 
  const popularityMovies = ref([]);
  const topRatedMovies = ref([]);
  const nowRunningMovies = ref([]);
  const randomMovies = ref([])
  const articles = ref([])
  
  const isAuthenticated = computed(() => !!token.value);
  const router = useRouter();
  const API_URL = 'http://127.0.0.1:8000';
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })


  const fetchUser = () => {
    if (token.value) {
      return axios.get(`${API_URL}/api/v1/accounts/user/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      .then((response) => {
        user.value = response.data;
      })
      .catch((error) => {
        console.error('사용자 정보를 불러오지 못했습니다.', error);
        // logout(); // 실패 시 로그아웃 처리
      });
    } 
  };
  
  const fetchPopularityMovies = () => {
    axios ({
      method: 'GET',
      url: `${API_URL}/api/v1/movies/recommend/popularity/`,
    })
    .then(response => {
      popularityMovies.value = response.data
    })
    .catch(error => {
      console.error('Now Running Movies Fetch Error:', error);
    });
  };
  
  const fetchTopRatedMovies = () => {
    axios ({
      method: 'GET',
      url: `${API_URL}/api/v1/movies/recommend/average/`,
    })
    .then(response => {
      topRatedMovies.value = response.data
    })
    .catch(error => {
      console.error('Now Running Movies Fetch Error:', error);
    });
  };

  const fetchNowRunningMovies = () => {
    axios ({
      method: 'GET',
      url: `${API_URL}/api/v1/movies/recommend/latest/`,
    })
    .then(response => {
      nowRunningMovies.value = response.data
    })
    .catch(error => {
      console.error('Now Running Movies Fetch Error:', error);
    });
  };

  const fetchRandomMovies = () => {
    axios({
      method: 'GET',
      url: `${API_URL}/api/v1/movies/recommend/random`,
    })
    .then(response => {
      randomMovies.value = response.data
    })
    .catch(error => {
      console.error('Random Movies Error', error)
    })
  }

  const signUp = (payload) => {
    const { username, email, password1, password2, profile_image } = payload;
  
    // Create a FormData object and append the fields
    const formData = new FormData();
    formData.append('username', username);
    formData.append('email', email);
    formData.append('password1', password1);
    formData.append('password2', password2);
    if (profile_image) {
      formData.append('profile_image', profile_image);
    }
  
    axios({
      method: 'post',
      url: `${API_URL}/api/v1/accounts/signup/`,
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then((response) => {
      console.log(response);
      const password = password1;
      logIn({ username, password });
    })
    .catch((error) => {
      console.error(error);
    });
  };

  const getArticles = () => {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/`
    })
      .then(response => {
        console.log(response)
        console.log(response.data)
        articles.value = response.data
      })
      .catch(error => {
        console.log(error)
      })
    }

  
  const logIn = function (payload) {
      // 1. 사용자 입력 데이터를 받아
      const { username, password } = payload
      // 2. axios로 django에 요청을 보냄
      axios({
        method: 'post',
        url: `${API_URL}/api/v1/accounts/login/`,
        data: {
          username, password
        }
      })
        .then((response) => {
          console.log('로그인 성공!')
          // 3. 로그인 성공 후 응답 받은 토큰을 저장
          token.value = response.data.key
          router.push({ name : 'HomePageView' })
        })
          .then((response) => {
            axios({
              method: 'GET',
              url: `${API_URL}/api/v1/accounts/get_user/`,
              headers: {
                Authorization: `Token ${token.value}`
              }
            })
            .then((response) => {
              user.value = response.data
              console.log(user.value)
              router.push({ name: 'HomePageView' })
            })
            .catch((error) => {
              console.log(error)
            })
          })
        .catch((error) => {
          console.log(error)
        })
    }

  const logout = () => {
    user.value = null;
    token.value = null;
    localStorage.removeItem('user','token');
  };

  return { 
    user, 
    articles,
    token, 
    topRatedMovies, 
    nowRunningMovies, 
    popularityMovies,
    randomMovies,
    isAuthenticated, 
    logout,
    fetchUser, 
    fetchTopRatedMovies, 
    fetchNowRunningMovies,
    fetchPopularityMovies,
    fetchRandomMovies,
    getArticles,
    signUp, 
    logIn, 
    API_URL,
    isLogin 

  };
}, { persist: true });

