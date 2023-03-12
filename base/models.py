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


class Admin(models.Model):
    users = (
        ('Ilona', 'Илона'),
        ('Dan', 'Данил'),
        ('Lex', 'Лёха'),
        ('Andrew', 'Андрей'),
    )
    name = models.CharField(choices=users, max_length=100)
    telegram_id = models.CharField(max_length=150)
    iqos = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    troll_mode = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AdminTroll(models.Model):
    admin = models.ForeignKey(Admin, models.CASCADE)
    text = models.TextField()


class Fandom(models.Model):
    name = models.CharField(max_length=150)


class Genre(models.Model):
    name = models.CharField(max_length=150)


class Setting(models.Model):
    tg_api = models.CharField(max_length=300)
    threads = models.PositiveIntegerField(default=0)


class ChatGPTCredentials(models.Model):
    login = models.CharField(max_length=150)
    password = models.CharField(max_length=149)
