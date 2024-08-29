from rest_framework import serializers
from ..models import Movie, Actor


class ActorListSerializer(serializers.ModelSerializer):

  class Meta:
    model = Actor
    fields = '__all__'


  