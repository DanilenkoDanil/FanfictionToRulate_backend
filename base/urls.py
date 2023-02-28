from django.contrib import admin
from django.urls import path, include
from base.views import Test
from rest_framework import routers
from base.views import FandomListAPIView, GenreListAPIView, BookListAPIView, ChapterListAPIView, \
    ChapterRetrieveAPIView, CheckBookAPIView

urlpatterns = [
    path('fandoms/', FandomListAPIView.as_view()),
    path('genres/', GenreListAPIView.as_view()),
    path('books/', BookListAPIView.as_view()),
    path('chapters/<int:pk>/', ChapterListAPIView.as_view()),
    path('chapter_text/<int:pk>/', ChapterRetrieveAPIView.as_view()),
    path('check_book/', CheckBookAPIView.as_view()),
]
