from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.bouldering_home, name='bouldering-home'),
]