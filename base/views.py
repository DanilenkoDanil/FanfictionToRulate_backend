from base.models import Book, Chapter, User
from django.http import JsonResponse
from django.views import View
from base.parser import parse_book
from background_task import background
from background_task.models import Task


class Test(View):

    def get(self, request, *args, **kwargs):
        parse_book('https://m.fanfiction.net/s/13162660/1/Magic-Knows-No-Boundaries-But-Those-We-Believe-In', 'f', 'd')
        return JsonResponse({'data': check_link_presence("gdg")})


def check_link_presence(url: str) -> bool:
    try:
        Book.objects.get(link=url)
        return True
    except Book.DoesNotExist:
        return False




