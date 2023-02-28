from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from base.models import Fandom, Genre, Book, Chapter


class FandomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Fandom
        fields = ['id', 'name']


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'genre', 'fandom', 'status']


class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'name', 'status']


class ChapterTextSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'name', 'text', 'status']