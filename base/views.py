from base.models import Book, Fandom, Genre, Chapter, Setting
from base.serializers import FandomSerializer, GenreSerializer, BookSerializer, ChapterSerializer, ChapterTextSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from base.parser import parse_book
from base.chat_gpt import translate_chapter


class FandomListAPIView(generics.ListAPIView):
    queryset = Fandom.objects.all()
    serializer_class = FandomSerializer


class GenreListAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ChapterListAPIView(generics.ListAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        return Chapter.objects.filter(book__id=self.kwargs['pk'])


class ChapterRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ChapterTextSerializer

    def get_queryset(self):
        return Chapter.objects.filter(id=self.kwargs['pk'])


class CheckBookAPIView(APIView):
    queryset = Book.objects.all()

    def post(self, request, format=None):
        try:
            Book.objects.get(link=request.data['url'])
            return Response(status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ParseBookAPIView(APIView):
    queryset = Book.objects.all()

    def post(self, request, format=None):
        try:
            parse_book(request.data['url'], request.data['fandom'], request.data['genre'])
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TranslateChapterAPIView(APIView):
    queryset = Book.objects.all()

    def get(self, request, pk, format=None):
        try:
            translate_chapter(pk)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
