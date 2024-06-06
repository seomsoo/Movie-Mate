from rest_framework import serializers
from django.contrib.auth import get_user_model

from ..models import Article
from .comment import CommentSerializer

User = get_user_model()


# 단일 게시글 정보
class ArticleSerializer(serializers.ModelSerializer):

  class UserSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields = ('pk', 'username',)

  comments = CommentSerializer(many=True, read_only=True)
  user = UserSerializer(read_only=True)
  like_users = UserSerializer(read_only=True, many=True)

  like_count = UserSerializer(read_only=True, many=True)
  comment_count = serializers.IntegerField(source='comments.count', read_only=True)

  class Meta:
    model = Article
    fields = ('pk', 'title', 'user', 'comment_count', 'comments', 'like_count', 'created_at', 'like_users', 'content',)


# 게시글 목록
class ArticleListSerializer(serializers.ModelSerializer):

  class UserSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields = ('pk', 'username',)
  user = UserSerializer(read_only=True)
  comment_count = serializers.IntegerField()
  like_count = serializers.IntegerField()

  class Meta:
    model = Article
    fields = ('pk', 'title', 'user', 'comment_count', 'like_count', 'created_at', 'content',)