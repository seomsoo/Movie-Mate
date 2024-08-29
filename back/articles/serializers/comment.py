from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'profile_image',)

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # 여기에 UserSerializer 포함

    class Meta:
        model = Comment
        fields = ('pk', 'user', 'content', 'article', 'created_at', 'updated_at',)
        read_only_fields = ('article', 'user',)
