from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Article, Comment
from .serializers.article import ArticleListSerializer, ArticleSerializer
from .serializers.comment import CommentSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def article_list_or_create(request):

  def article_list():
    # comment 개수
    articles = Article.objects.annotate(
      comment_count = Count('comments', distinct=True),
      like_count = Count('like_users', distinct=True)
    ).order_by('-pk')
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data)
  
  def create_article():
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(user=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
  if request.method == 'GET':
    return article_list()
  elif request.method == 'POST':
    return create_article()
  

@api_view(['GET', 'PUT', 'DELETE'])
def article_detail_or_update_or_delete(request, article_pk):
  article = get_object_or_404(Article, pk=article_pk)

  if request.method == 'GET':
    serializer = ArticleSerializer(article)
    return Response(serializer.data)
  
  elif request.method == 'PUT':
    if request.user == article.user:
      serializer = ArticleSerializer(instance=article, data=request.data)
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_403_FORBIDDEN)

  elif request.method == 'DELETE':
    if request.user == article.user:
      article.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def like_article(request, article_pk):
  article = get_object_or_404(Article, pk=article_pk)
  user = request.user
  if article.like_users.filter(pk=user.pk).exists():
    article.like_users.remove(user)
    serializer = ArticleSerializer(article)
    return Response(serializer.data)
  else:
    article.like_users.add(user)
    serializer = ArticleSerializer(article)
    return Response(serializer.data)
  

@api_view(['GET', 'POST'])
def create_comment(request, article_pk):
    user = request.user
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article, user=user)
            comments = article.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
  

@api_view(['PUT', 'DELETE'])
def comment_update_or_delete(request, article_pk, comment_pk):
  article = get_object_or_404(Article, pk=article_pk)
  comment = get_object_or_404(Comment, pk=comment_pk)

  def update_comment():
    if request.user == comment.user:
      serializer = CommentSerializer(instance=comment, data=request.data)
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
      
  def delete_comment():
    if request.user == comment.user:
      comment.delete()
      comments = article.comments.all()
      serializer = CommentSerializer(comments, many=True)
      return Response(serializer.data)
    
  if request.method == 'PUT':
    return update_comment()
  elif request.method == 'DELETE':
    return delete_comment()