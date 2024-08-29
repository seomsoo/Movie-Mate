from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movies_list),
    path('<int:movie_pk>/', views.movie_detail),
    path('<int:movie_pk>/like/', views.like_movie),
    path('<int:user_pk>/', views.user_like_movie),
    path('<int:movie_pk>/reviews/', views.movie_reviews),
    path('reviews/<int:review_pk>/', views.update_or_delete_review),
    path('<int:movie_pk>/rating/', views.create_rating),
    path('<int:movie_pk>/rating/<int:rating_pk>/', views.rating_update_or_delete),
    path('search/<str:movie_name>/', views.search_movie),

    path('recommend/latest/', views.latest), # 최신순
    path('recommend/popularity/', views.popularity), # 인기순  
    path('recommend/average/', views.vote_average), # 평점 
    path('recommend/random/', views.random), # 랜덤

    path('genres/', views.genres_list),
    path('genre/<int:genre_pk>/', views.genre_detail),
    path('genre/<int:genre_pk>/latest/', views.genre_latest),
    path('genre/<int:genre_pk>/popularity/', views.genre_popularity),
    path('genre/<int:genre_pk>/vote-average/', views.genre_vote_average),
    path('genre/<int:genre_pk>/vote-count/', views.genre_vote_count),

    path('recommend/', views.movie_recommendation),
]
