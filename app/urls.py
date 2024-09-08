from django.urls import path

from app import views

urlpatterns = [
    path('magic/', views.magic, name='magic'),
]
