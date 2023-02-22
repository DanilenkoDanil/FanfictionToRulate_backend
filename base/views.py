from base.models import Book, Fandom, Genre
from django.http import JsonResponse
from django.views import View
from base.parser import parse_book
from django.db import models


class Test(View):

    def get(self, request, *args, **kwargs):
        parse_book('https://m.fanfiction.net/s/13162660/1/Magic-Knows-No-Boundaries-But-Those-We-Believe-In', 'f', 'd')
        return JsonResponse({'data': check_link_presence("gdg")})


class BookTypeInterface():
    def __init__(self):
        self.model = models.Model

    def collect_type(self):
        genre_names = []
        for model_object in range(self.model.objects.all()):
            genre_names.append(model_object.name)

        return genre_names


class BookFandomCollector(BookTypeInterface):
    def __init__(self):
        super(BookFandomCollector, self).__init__()
        self.model = Fandom


class BookGenreCollector(BookTypeInterface):
    def __init__(self):
        super(BookGenreCollector, self).__init__()
        self.model = Genre


def check_link_presence(url: str) -> bool:
    try:
        Book.objects.get(link=url)
        return True
    except Book.DoesNotExist:
        return False


print(Fandom.objects.all())