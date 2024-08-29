from rest_framework import serializers
from django.contrib.auth import get_user_model
from articles.models import Article
from movies.models import Movie
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

User = get_user_model()

# 사용자 프로필에 들어가는 정보
class ProfileSerializer(serializers.ModelSerializer):

  class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
      model = Article
      fields = '__all__'

  class MovieSerializer(serializers.ModelSerializer):
    class Meta:
      model = Movie
      fields = '__all__'

  like_articles = ArticleSerializer(many=True)
  articles = ArticleSerializer(many=True)
  like_movies = MovieSerializer(many=True)
  followers_count = serializers.IntegerField(source='followers.count', read_only=True)
  followings_count = serializers.IntegerField(source='followings.count', read_only=True)
  
  class Meta:
    model = User
    fields = ('pk', 'username', 'email', 'followers_count', 'followings_count', 'like_articles', 'articles', 'like_movies', 'profile_image',)




# 유저 정보
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'


# 회원가입 정보
class CustomRegisterSerializer(RegisterSerializer):
  # 기본 설정 필드: username, password, email
  # 추가 설정 필드: profile_image
  profile_image = serializers.ImageField(use_url=True, required=False)

  def get_cleaned_data(self):
    data = super().get_cleaned_data()
    data['profile_image'] = self.validated_data.get('profile_image', '')

    return data
