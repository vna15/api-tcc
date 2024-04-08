from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
   # path('', views.get_users, name='get_all_users'),
   # path('user/<str:email>', views.get_by_email)
   path('', views.user_manager),
]
