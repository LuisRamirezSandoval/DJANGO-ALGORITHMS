from django.shortcuts import render
from .models import Post

# Create your views here.

def index(request):
    return render(request, 'app1/index.html', cont={})

def post_list(request):
    consulta = Post.objects.all()
    cont = {'datos':consulta}
    datos = list(Post.objects.all())
    suma=[]
    for dato in datos:
        val = dato.num1+dato.num3+dato.num4
        suma.append(val)
    cont['suma']=suma
    # print(cont)
    return render(request, 'app1/post_list.html', cont)

def hola_mundo(request):
    cont = {'mensaje':['hola mundo']}
    return render(request, 'app1/hola_mundo.html', cont)