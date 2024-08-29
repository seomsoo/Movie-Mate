from django.db import models
from django.conf import settings

class Actor(models.Model):
    name = models.CharField(max_length=50, null=False)

class Genre(models.Model):
    name = models.CharField(max_length=50, null=False)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    released_date = models.DateField(null=True, blank=True)
    actors = models.ManyToManyField(Actor, related_name='movies')
    vote_average = models.FloatField(null=True, blank=True)
    vote_count = models.IntegerField(null=True)
    overview = models.TextField(null=True, blank=True)
    runtime = models.IntegerField(null=True)
    popularity = models.FloatField(null=True, blank=True)
    poster_path = models.CharField(max_length=100, null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    words = models.TextField(null=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')

class MovieComment(models.Model):
    STAR_CHOICES = [
        ('5', "★★★★★"),
        ('4', "★★★★"),
        ('3', "★★★"),
        ('2', "★★"),
        ('1', "★"),
        (None, '선택')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movie_comments')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_comments')
    rating = models.CharField(max_length=10, choices=STAR_CHOICES)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

