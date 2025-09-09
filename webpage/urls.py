# otop_app/urls.py
from django.urls import path
from . import views

from django.contrib import admin
from django.urls import path
from webpage import views

urlpatterns = [
    path('map/', views.map_view, name='otop_map'),
]
