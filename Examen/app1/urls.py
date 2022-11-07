from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.post_list, name='post_list'),
    path('hola_mundo/', views.hola_mundo, name='hola_mundo'),
]