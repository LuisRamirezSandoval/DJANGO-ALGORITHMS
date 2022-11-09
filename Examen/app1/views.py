from django.shortcuts import render
from .models import Post
import math
# Create your views here.

def index(request):
    return render(request, 'app1/index.html', {})

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

def algoritmo_knn(request):
    if request.method == 'GET':
        print('enviando datos')
        return render(request, 'app1/knn.html', {})
    else:
        x = int(request.POST['x'])
        y = int(request.POST['y'])
        z = int(request.POST['z'])
        db = Post.objects.all()
        print('obteniendo datos.....')
        print(x,y,z)
        distancia = []
        for i in range(len(db)):
            val = math.sqrt(((x-db[i].num1)**2)+((y-db[i].num3)**2)+((z-db[i].num4)**2))
            #print(val)
            distancia.append((db[i].num2, val))
        #print(distancia)
        cont = { 'dist': distancia}
    return render(request, 'app1/knn.html', cont)

def hola_mundo(request):
    cont = {'mensaje':['hola mundo']}
    return render(request, 'app1/hola_mundo.html', cont)