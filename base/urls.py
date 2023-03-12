from django.urls import path
from base.views import FandomListAPIView, GenreListAPIView, BookListAPIView, ChapterListAPIView, \
    ChapterRetrieveAPIView, CheckBookAPIView, ParseBookAPIView, TranslateChapterAPIView, AdminListAPIView, \
    AdminTrollListAPIView, TrollIlonaTwoHoursAPIView

urlpatterns = [
    path('fandoms/', FandomListAPIView.as_view()),
    path('genres/', GenreListAPIView.as_view()),
    path('admins/', AdminListAPIView.as_view()),
    path('books/', BookListAPIView.as_view()),
    path('chapters/<int:pk>/', ChapterListAPIView.as_view()),
    path('chapter_text/<int:pk>/', ChapterRetrieveAPIView.as_view()),
    path('troll_admin/<int:pk>/', AdminTrollListAPIView.as_view()),
    path('check_book/', CheckBookAPIView.as_view()),
    path('parse_book/', ParseBookAPIView.as_view()),
    path('troll_ilona/', TrollIlonaTwoHoursAPIView.as_view()),
    path('translate_chapter/<int:pk>/', TranslateChapterAPIView.as_view()),

]
