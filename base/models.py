from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=150)
    genre = models.CharField(max_length=50)
    fandom = models.CharField(max_length=50)
    link = models.CharField(max_length=150)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=150)
    text = models.TextField()
    status = models.BooleanField(default=False)
    data = models.DateTimeField(auto_now=True)


class User(models.Model):
    name = models.CharField(max_length=150)
    telegram_id = models.CharField(max_length=150)
    iqos = models.BooleanField(default=False)
    status = models.BooleanField(default=False)


class Fandom(models.Model):
    name = models.CharField(max_length=150)


class Genre(models.Model):
    name = models.CharField(max_length=150)
