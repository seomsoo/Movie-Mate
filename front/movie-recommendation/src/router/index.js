import HomePageView from '@/views/movies/HomePageView.vue'
import SignUpView from '@/views/accounts/SignUpView.vue'
import LoginView from '@/views/accounts/LoginView.vue'
import ProfileView from '@/views/accounts/ProfileView.vue'
import ProfileEditView from '@/views/accounts/ProfileEditView.vue'
import CommunityPageView from '@/views/community/CommunityPageView.vue'
import EditPostView from '@/views/community/EditPostView.vue'
import AiRecommendationView from '@/views/movies/AiRecommendationView.vue'
import SearchResultView from '@/views/movies/SearchResultView.vue'
import DetailPageView from '@/views/movies/DetailPageView.vue'
import GenrePageView from '@/views/movies/GenrePageView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import CreatePostView from '@/views/community/CreatePostView.vue'
import DetailPostView from '@/views/community/DetailPostView.vue'
import MovieReviewForm from '@/components/movies/MovieReviewForm.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePageView',
      component: HomePageView
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LoginView',
      component: LoginView
    },
    {
      path: '/profile/:username',
      name: 'ProfileView',
      component: ProfileView
    },
    {
      path: '/profile/edit/:username',
      name: 'ProfileEditView',
      component: ProfileEditView
    },
    {
      path: '/community',
      name: 'CommunityPageView',
      component: CommunityPageView
    },
    {
      path: '/edit/:id',
      name: 'EditPostView',
      component: EditPostView
    },
    {
      path: '/openai',
      name: 'AiRecommendationView',
      component: AiRecommendationView
    },
    {
      path: '/search',
      name: 'SearchResultView',
      component: SearchResultView
    },
    {
      path: '/:movieId',
      name: 'DetailPageView',
      component: DetailPageView
    },
    {
      path: '/genre',
      name: 'GenrePageView',
      component: GenrePageView
    },
    {
      path: '/articles/:id',
      name: 'DetailPostView',
      component: DetailPostView
    },
    {
      path: '/createpost',
      name: 'CreatePostView',
      component: CreatePostView
    },
    {
      path: '/movies/:movie_pk/rating/',
      name: 'MovieRating',
      component: MovieReviewForm
    }
  ]
})
import { useMovieStore } from '@/stores/movie'

router.beforeEach((to, from) => {
  const store = useMovieStore()
  // if (to.name === 'DetailPageView' || to.name === 'GenrePageView'|| to.name === 'AiRecommendationView' 
  //    && store.isLogin === false) {
  //     window.alert('로그인 해주세요!')
  //     return { name: 'LoginView'}
  //   }


  if ((to.name === 'SignUpView' || to.name === 'LoginView') && (store.isLogin === true)) {
    window.alert('이미 로그인 했습니다.')
    return { name: 'HomePageView' }
  }
})


export default router
