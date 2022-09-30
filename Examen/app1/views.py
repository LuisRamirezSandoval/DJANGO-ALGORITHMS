from django.shortcuts import render
from .models import Post

# Create your views here.

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