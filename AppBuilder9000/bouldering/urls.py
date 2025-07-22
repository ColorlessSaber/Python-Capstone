from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.bouldering_home, name='bouldering-home'),
    path('log-in/', views.login_page, name='login'),
    path('new-account/', views.new_account, name='new-account'),
    path('user-climb-logs/', views.load_user_climbs, name='user-climb-logs'),
]