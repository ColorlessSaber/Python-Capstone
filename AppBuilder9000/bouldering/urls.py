from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.bouldering_home, name='bouldering-home'),
    path('log-in/', views.login_page, name='login'),
    path('new-account/', views.new_account, name='new-account'),
    path('user-<int:user_pk>/climb-logs/', views.load_user_climbs, name='user-climb-logs'),
    path('user-<int:user_pk>/new-climb-log/', views.create_new_climb_log, name='new-climb-log'),
    path('user-<int:user_pk>/climb-log-<int:climb_log_pk>/', views.load_climb_details, name='climb-log-details'),
]