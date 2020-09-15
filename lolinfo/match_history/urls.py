from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('expand/', views.expand, name="expand"),
]