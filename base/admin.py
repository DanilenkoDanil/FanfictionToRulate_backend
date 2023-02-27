from django.contrib import admin
from .models import Book, Chapter, Admin, Fandom, Genre, Setting, ChatGPTCredentials


@admin.register(Book)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'fandom', 'link', 'status')
    search_fields = ('name', 'status')


@admin.register(Chapter)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('book', 'number', 'name', 'status', 'data')
    search_fields = ('book', 'name')


@admin.register(Admin)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'iqos', 'status')


@admin.register(Fandom)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Genre)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('tg_api', 'threads')


@admin.register(ChatGPTCredentials)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('login', 'password')
