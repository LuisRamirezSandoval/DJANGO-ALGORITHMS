from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('hola/', views.hola_mundo, name='hola_mundo')
]