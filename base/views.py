from base.models import Book, Fandom, Genre, Chapter, Setting
from django.http import JsonResponse
from django.views import View
from django.db import models
from abc import ABC, abstractmethod
from base.serializers import FandomSerializer, GenreSerializer, BookSerializer, ChapterSerializer, ChapterTextSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status



class Test(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({'data': check_link_presence("gdg")})


class BookTypeInterface:
    def __init__(self):
        self.model = models.Model

    def collect_type(self) -> list:
        type_names = []
        for model_object in self.model.objects.all():
            type_names.append(model_object.name)

        return type_names


class BookValueAbstract(ABC):
    def __init__(self):
        self.model = models.Model

    @abstractmethod
    def collect_value(self, name: str):
        pass


class BooksCollector(BookValueAbstract):
    def __init__(self):
        super().__init__()
        self.model = Book

    def collect_value(self, name: str) -> list:
        book_name = []
        for model_object in self.model.objects.filter(name=name):
            book_str = str(model_object.name) + ' ' + str(model_object.status)
            book_name.append(book_str)
        return book_name

    def collect_list_books(self):
        book_list = []
        for model_object in self.model.objects.all():
            book_str = str(model_object.name) + ' ' + str(model_object.status)
            book_list.append(book_str)
        return book_list


class ChaptersCollector(BookValueAbstract):
    def __init__(self):
        super().__init__()
        self.model = Chapter

    def collect_value(self, name: str) -> list:
        books_list = []
        try:
            book = Book.objects.get(name=name)
        except Book.DoesNotExist:
            return books_list
        for model_object in self.model.objects.filter(book=book):
            book_str = str(model_object.number) + ' ' + str(model_object.name) + ' ' + str(model_object.status)
            books_list.append(book_str)
        return books_list


class BookFandomCollector(BookTypeInterface):
    def __init__(self):
        super(BookFandomCollector, self).__init__()
        self.model = Fandom


class BookGenreCollector(BookTypeInterface):
    def __init__(self):
        super(BookGenreCollector, self).__init__()
        self.model = Genre


class FandomListAPIView(generics.ListAPIView):
    queryset = Fandom.objects.all()
    serializer_class = FandomSerializer


class GenreListAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CheckBookAPIView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    queryset = Book.objects.all()

    def post(self, request, format=None):
        print(request.data)
        try:
            Book.objects.get(link=request.data['url'])
            return Response(status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChapterListAPIView(generics.ListAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        return Chapter.objects.filter(book__id=self.kwargs['pk'])


class ChapterRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ChapterTextSerializer

    def get_queryset(self):
        return Chapter.objects.filter(id=self.kwargs['pk'])


def get_tg_api_key() -> str:
    api_key = ''
    try:
        return Setting.objects.get(id=1).tg_api
    except Setting.DoesNotExist:
        return api_key


def get_chapter_text(name: str, number: int) -> str:
    chapter = ''
    try:
        book = Book.objects.get(name=name)
    except Book.DoesNotExist:
        return chapter
    try:
        chapter_object = Chapter.objects.get(book=book, number=number)
    except Chapter.DoesNotExist:
        return chapter
    chapter = chapter_object.text
    return chapter


def check_link_presence(url: str) -> bool:
    try:
        Book.objects.get(link=url)
        return True
    except Book.DoesNotExist:
        return False
