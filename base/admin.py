from django.contrib import admin
from .models import Book, Chapter, User


@admin.register(Book)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'fandom', 'link', 'status')
    search_fields = ('name', 'status')


@admin.register(Chapter)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('book', 'number', 'name', 'status', 'data')
    search_fields = ('book', 'name')


@admin.register(User)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'iqos', 'status')

