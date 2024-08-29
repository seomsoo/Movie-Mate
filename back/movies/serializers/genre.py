from rest_framework import serializers
from ..models import Movie, Genre


class GenreListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

  class MovieSerializer(serializers.ModelSerializer):
    class Meta:
      model = Movie
      fields = ('title', 'poster_path', 'released_date', 'vote_count', 'popularity', 'vote_average', 'id',)

  movies = MovieSerializer(many = True, read_only = True)

  class Meta:
    model = Genre
    fields = '__all__'