from django.shortcuts import get_list_or_404, get_object_or_404
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from datetime import date
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Actor, Movie, Genre, MovieComment
from rest_framework.permissions import IsAuthenticated
from accounts.models import User

from .serializers.genre import GenreSerializer, GenreListSerializer
from .serializers.movie import MovieSerializer, MovieCommentSerializer, UserLikeMovieListSerializer, MovieSearchSerializer, MovieListSerializer, UserChoiceSimilarMovieSerializer, RecommendMovie

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from jellyfish import jaro_winkler_similarity

import openai

# TMDB_API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1ZmVmMGYyZmMxYmVjMWQwNTI4MTkzNmMzMzJjMDQxMiIsInN1YiI6IjY2M2Q4ZWE5YWIwZDNjOWY5YzUwZDY0NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.k9KRXAEe9cUbxgzudrpXI5A-bdGh9yPS2atfI4qM41Y'
openai.api_key = settings.OPENAI_API_KEY

@api_view(['POST'])
@permission_classes([AllowAny])
def movie_recommendation(request):
    user_input = request.data.get('input', '')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who provides movie recommendations in Korean."},
            {"role": "user", "content": f"영화 추천해줘: {user_input}"}
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    recommendation = response.choices[0].message['content'].strip()
    return Response({"recommendation": recommendation})

# Create your views here.
@api_view(['GET'])
def movies_list(request):
  movies = get_list_or_404(Movie)
  serializer = MovieListSerializer(movies, many=True)
  return Response(serializer.data)


@api_view(['GET'])
def movie_detail(request, movie_pk):
  movie = get_object_or_404(Movie, pk=movie_pk)
  serializer = MovieSerializer(movie)
  return Response(serializer.data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_movie(request, movie_pk):
  user = request.user
  movie = get_object_or_404(Movie, movie_pk)
  if movie.like_users.filter(username=user.username).exists():
    movie.like_users.remove(user)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)
  else:
    movie.like_users.add(user)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)
  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_like_movie(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    liked_movies = user.like_movies.all()
    serializer = MovieListSerializer(liked_movies, many=True)
    return Response(serializer.data)

  # movie_keys = [data['pk'] for data in serializer.data.get('like_movies')]

  # idx = []
  # for key in movie_keys:
  #   for i in range(len(movies_serializer.data)):
  #     if key == movies_serializer.data[i]['pk']:
  #       idx.append(i)
  #       break

  # xMovie = [data.get('words') for data in movies_serializer.data]

  # result = recommend_movies_names(xMovie, idx, movies_serializer)

  # final_movie = [get_object_or_404(Movie, pk=i) for i in result]
  # final_serializer = UserChoiceSimilarMovieSerializer(final_movie, many=True)

  # return Response(final_serializer.data)



def recommend_movies_names(xMovie, idx, movies):
  # 불용어 제거
  countVec = CountVectorizer(max_features=10000, stop_words='english')

  # 영화 키워드 벡터라이징
  dataVectors = countVec.fit_transform(xMovie).toarray()

  # 코사인 유사도
  similarity = cosine_similarity(dataVectors)

  # 유사도 내림차순 5개 영화 인덱스
  idx_collection = []
  for i in idx:
    distances = similarity[i]
    listofMovies = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:7]
    idx_collection.extend(listofMovies)

  # 인덱스 pk로 바꾸기
  pk_collection = []
  for idx in idx_collection:
    pk_collection.append(movies.data[idx[0]]['pk'])

  return pk_collection


@api_view(['GET'])
def movie_reviews(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = MovieComment.objects.filter(movie=movie)
    serializer = MovieCommentSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
def update_or_delete_review(request, review_pk):
    review = get_object_or_404(MovieComment, pk=review_pk)
    
    if request.user != review.user:
        return Response({'detail': '권한이 없습니다.'}, status=403)

    if request.method == 'PUT':
        serializer = MovieCommentSerializer(review, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=204)
    
@api_view(['POST'])
def create_rating(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    rating = movie.movie_comments.filter(user=user).first()  # 여기서 movie_comments로 변경
    serializer = MovieCommentSerializer(data=request.data)

    if not rating:
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=user)

            ratings = movie.movie_comments.all()  # 여기서 movie_comments로 변경
            serializer = MovieCommentSerializer(ratings, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    


@api_view(['PUT', 'DELETE'])
def rating_update_or_delete(request, movie_pk, rating_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    rating = get_object_or_404(MovieComment, pk=rating_pk)

    def update_rating():
        if request.user == rating.user:
            serializer = MovieCommentSerializer(instance=rating, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                ratings = movie.ratings.all()
                serializer = MovieCommentSerializer(ratings, many=True)
                return Response(serializer.data)

    def delete_rating():
        if request.user == rating.user:
            rating.delete()
            ratings = movie.ratings.all()
            serializer = MovieCommentSerializer(ratings, many=True)
            return Response(serializer.data)
    
    if request.method == 'PUT':
        return update_rating()
    elif request.method == 'DELETE':
        return delete_rating()
    


@api_view(['GET'])
def search_movie(request, movie_name):
   movies = get_list_or_404(Movie)
   serializer = MovieSearchSerializer(movies, many=True)
   serializer = search(serializer.data, movie_name)
   return Response(serializer[:16])


def search(lst, keyword):
  fetch_data = []
  for data in lst:
    tmp = {'pk': 0, 'title': '', 'poster_path': '', 'similarity': ''}
    tmp['pk'] = data['pk']
    tmp['title'] = data['title']
    tmp['poster_path'] = data['poster_path']
    tmp['similarity'] = jaro_winkler_similarity(keyword, data['title'])
    fetch_data.append(tmp)

  fetch_data.sort(key=lambda x : -x['similarity'])
  return fetch_data



### 영화 추천(인기순, 평점순, 개봉일순(최근))
@api_view(['GET'])
def popularity(request):
    popularity_movies = Movie.objects.order_by('-popularity')[:30]
    serializer = RecommendMovie(popularity_movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def vote_average(request):
    vote_average_movies = Movie.objects.order_by('-vote_average')[:30]
    serializer = RecommendMovie(vote_average_movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def latest(request):
  today = timezone.now().date()
  latest_movies = Movie.objects.filter(released_date__lt=today).order_by('-released_date')[:30]
  serializer = RecommendMovie(latest_movies, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def random(request):
    random_movies = Movie.objects.order_by('?')[:10]
    serializer = RecommendMovie(random_movies, many=True)
    return Response(serializer.data)


# 모든 장르
@api_view(['GET'])
def genres_list(request):
   genres = Genre.objects.all()
   serializer = GenreListSerializer(genres, many=True)
   return Response(serializer.data)


# 세부 장르의 영화들
@api_view(['GET'])
def genre_detail(request, genre_pk):
  genre = get_object_or_404(Genre, pk=genre_pk)
  serializer = GenreSerializer(genre)
  return Response(serializer.data)


@api_view(['GET'])
def genre_latest(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)
    today = timezone.now().date()

    
    sort_by = request.GET.get('sort_by', 'released_date')
    
    sort_fields = {
        'released_date': '-released_date',
        'vote_count': '-vote_count',
        'popularity': '-popularity',
        'vote_average': '-vote_average',
    }
    sort_field = sort_fields.get(sort_by, '-released_date')
    
    movies = genre.movies.filter(released_date__lt=today).order_by(sort_field)[:50]
    
    genre_serializer = GenreSerializer(genre)
    genre_data = genre_serializer.data
    
    movie_serializer = GenreSerializer.MovieSerializer(movies, many=True)
    genre_data['movies'] = movie_serializer.data
    
    return Response(genre_data)




@api_view(['GET'])
def genre_popularity(request, genre_pk):
  genre = get_object_or_404(Genre, pk=genre_pk)
  today = timezone.now().date()
    
  sort_by = request.GET.get('sort_by', 'popularity')
  
  sort_fields = {
      'released_date': '-released_date',
      'vote_count': '-vote_count',
      'popularity': '-popularity',
      'vote_average': '-vote_average',
  }
  sort_field = sort_fields.get(sort_by, '-popularity')
  
  movies = genre.movies.filter(released_date__lt=today).order_by(sort_field)[:50]
  
  genre_serializer = GenreSerializer(genre)
  genre_data = genre_serializer.data
  
  movie_serializer = GenreSerializer.MovieSerializer(movies, many=True)
  genre_data['movies'] = movie_serializer.data
  
  return Response(genre_data)


@api_view(['GET'])
def genre_vote_average(request, genre_pk):
  genre = get_object_or_404(Genre, pk=genre_pk)
  today = timezone.now().date()

  
  sort_by = request.GET.get('sort_by', 'vote_average')
  
  sort_fields = {
      'released_date': '-released_date',
      'vote_count': '-vote_count',
      'popularity': '-popularity',
      'vote_average': '-vote_average',
  }
  sort_field = sort_fields.get(sort_by, '-vote_average')
  
  movies = genre.movies.filter(released_date__lt=today).order_by(sort_field)[:50]
  
  genre_serializer = GenreSerializer(genre)
  genre_data = genre_serializer.data
    
  movie_serializer = GenreSerializer.MovieSerializer(movies, many=True)
  genre_data['movies'] = movie_serializer.data
  
  return Response(genre_data)


@api_view(['GET'])
def genre_vote_count(request, genre_pk):
  genre = get_object_or_404(Genre, pk=genre_pk)
  today = timezone.now().date()

    
  sort_by = request.GET.get('sort_by', 'vote_count')
  
  sort_fields = {
    'released_date': '-released_date',
    'vote_count': '-vote_count',
    'popularity': '-popularity',
    'vote_average': '-vote_average',
  }
  sort_field = sort_fields.get(sort_by, '-vote_count')
  
  movies = genre.movies.filter(released_date__lt=today).order_by(sort_field)[:50]
  
  genre_serializer = GenreSerializer(genre)
  genre_data = genre_serializer.data
  
  movie_serializer = GenreSerializer.MovieSerializer(movies, many=True)
  genre_data['movies'] = movie_serializer.data
  
  return Response(genre_data)