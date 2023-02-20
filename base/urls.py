from django.contrib import admin
from django.urls import path, include
from base.views import Test

urlpatterns = [
    path('test/', Test.as_view(), name='test'),
]


