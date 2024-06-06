from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Movie, Genre, Actor, MovieComment

User = get_user_model()

# 유저 정보
class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(use_url=True)  # 프로필 이미지 필드 추가

    class Meta:
        model = User
        fields = ('pk', 'username', 'profile_image')  # 필드에 profile_image 포함

# 좋아요 누른 영화
class UserLikeMovieListSerializer(serializers.ModelSerializer):

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('pk', 'poster_path',)

    like_movies = MovieSerializer(many=True)
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'like_movies')

# 검색한 영화와 비슷한 영화
class MovieSearchSerializer(serializers.ModelSerializer):

    similarity = serializers.FloatField(default=0)
    class Meta:
        model = Movie
        fields = ('pk', 'words', 'title', 'poster_path', 'similarity',)

# 댓글 및 평점
class MovieCommentSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = MovieComment
        fields = '__all__'
        read_only_fields = ('movie',)

# 단일 영화 상세 정보
class MovieSerializer(serializers.ModelSerializer):

    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = ('name',)

    class ActorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Actor
            fields = ('name',)

    genres = GenreSerializer(read_only=True, many=True)
    actors = ActorSerializer(read_only=True, many=True)
    like_users = UserSerializer(read_only=True, many=True)
    # comments = MovieCommentSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('vote_count',)

# 사용자가 선택 또는 좋아요 한 영화와 비슷한 영화
class UserChoiceSimilarMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'poster_path', 'pk')

## 영화 리스트
class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path')

## 영화 추천
class RecommendMovie(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'vote_average', 'poster_path', 'overview', 'released_date')
