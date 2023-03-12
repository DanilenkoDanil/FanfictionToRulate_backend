from base.models import Book, Fandom, Genre, Chapter, Setting, Admin, AdminTroll
from base.serializers import FandomSerializer, GenreSerializer, BookSerializer, ChapterSerializer, \
    ChapterTextSerializer, TrollAdminSerializer, AdminSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.parser import parse_book
from base.chat_gpt import translate_chapter
from base.tg_troll import send_troll
from rest_framework.permissions import IsAuthenticated


class FandomListAPIView(generics.ListAPIView):
    queryset = Fandom.objects.all()
    serializer_class = FandomSerializer
    permission_classes = [IsAuthenticated]


class GenreListAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class AdminListAPIView(generics.ListAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated]


class AdminTrollListAPIView(generics.ListAPIView):
    serializer_class = TrollAdminSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AdminTroll.objects.filter(admin__telegram_id=self.kwargs['pk'])


class ChapterListAPIView(generics.ListAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chapter.objects.filter(book__id=self.kwargs['pk'])


class ChapterRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ChapterTextSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chapter.objects.filter(id=self.kwargs['pk'])


class CheckBookAPIView(APIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            Book.objects.get(link=request.data['url'])
            return Response(status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ParseBookAPIView(APIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            parse_book(request.data['url'], request.data['fandom'], request.data['genre'])
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TrollIlonaTwoHoursAPIView(APIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            admin = Admin.objects.get(name='Ilona')
            send_troll(admin.telegram_id, schedule=60*120)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TranslateChapterAPIView(APIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            translate_chapter(pk)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
