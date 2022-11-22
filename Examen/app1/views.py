from django.shortcuts import render
from .models import Post
import math
from numpy import mean, var
import numpy as np
import random
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
        k = int(request.POST['k'])
        db = Post.objects.all()
        print('obteniendo datos.....')
        print(k,x,y,z)
        distancia = []
        for i in range(len(db)):
            val = math.sqrt(((x-db[i].num1)**2)+((y-db[i].num3)**2)+((z-db[i].num4)**2))
            #print(val)
            distancia.append((db[i].num2, val))
        #print(distancia)
        cont = { 'dist': distancia}
        #calculando distancia
        listK= distancia[:k]
        knn ={}
        letras=[]
        for i in listK:
            if i[0] in letras:
                knn[i[0]]+=1
            else:
                letras.append(i[0])
                knn[i[0]]=1
        cont['knn']=knn
    return render(request, 'app1/knn.html', cont)

def algoritmo_cbi(request):
    bd = list(Post.objects.all())
    new_bd = Post.objects.values('num2','num1','num3','num4').order_by('num2')
    letra=[]
    bd_final={}
    probabilidad=""
    cont=0
    for i in range(len(new_bd)):
        # si la letra no esta en el arreglo que haga esto, si no ignorar
        if bd[i].num2 in letra:
            cont+=1
            #print('ignorar letra')
            #letra.append(bd[i].num2)
        else:
            valor = Post.objects.filter(num2=bd[i].num2)
            letra.append(bd[i].num2)
            suma_num1=[]
            suma_num3=[]
            suma_num4=[]
            for j in list(valor):
                suma_num1.append(j.num1)
                suma_num3.append(j.num3)
                suma_num4.append(j.num4)
            media_num1=mean(suma_num1)
            varianza_num1= var(suma_num3)
            media_num3=mean(suma_num3)
            varianza_num3=var(suma_num3)
            media_num4=mean(suma_num4)
            varianza_num4=var(suma_num4)
            bd_final[bd[i].num2]=(media_num1,varianza_num1,media_num3,varianza_num3,media_num4,varianza_num4)
            #print('suma 1: ', valor)
    #print(len(letra))
    #print(bd_final)
    #print(bd_final)
    para_evidencia = {}
    if request.method == 'POST':
        x = int(request.POST['x'])
        y = int(request.POST['y'])
        z = int(request.POST['z'])
        p_letra = 1/len(bd_final)
        for l in range(len(bd_final)):
            #print(bd_final[letra[l]])
            para_evidencia[letra[l]]= pre_posteriori(bd_final[letra[l]][0],bd_final[letra[l]][2],bd_final[letra[l]][4],bd_final[letra[l]][1],bd_final[letra[l]][3],bd_final[letra[l]][5],x,y,z)

        evidcia = evidencia(para_evidencia,letra,p_letra)
        probabilidad = post_posteriori(para_evidencia,evidcia,letra)
        cont = {'letra': probabilidad}
    else:
        return render(request, 'app1/algoritmo_cbi.html', {})
    #print(para_evidencia)
    #print(evidcia)
    #print(letra)
    return render(request, 'app1/algoritmo_cbi.html', cont)

def pre_posteriori(media1,media3,media4,var1,var2,var3,x,y,z):
    p_num1 = (1/math.sqrt(2*math.pi*var1))* math.e*(pow(x-media1,2)/(2*var1))
    p_num3 = (1/math.sqrt(2*math.pi*var2))* math.e*(pow(y-media3,2)/(2*var2))
    p_num4 = (1/math.sqrt(2*math.pi*var3))* math.e*(pow(z-media4,2)/(2*var3))

    return (p_num1,p_num3,p_num4)

def post_posteriori(para_evidencia, evidencia,letras):
    rel = {}
    valores_rel =[]
    letra=""
    for i in range(len(para_evidencia)):
        val = (para_evidencia[letras[i]][0]*para_evidencia[letras[i]][1]*para_evidencia[letras[i]][2]) / evidencia
        rel[letras[i]]= val
        valores_rel.append(val)
    print(rel)
    maximo = max(valores_rel) 
    keys = list(rel.keys())  
    for j in range(len(rel)):
        if rel[letras[j]] == maximo:
            letra = letras[j]
    return letra
def evidencia(para_evidencia,letras,p_letra):
    rel=[]
    for i in range(len(para_evidencia)):
        rel.append(p_letra*para_evidencia[letras[i]][0]*para_evidencia[letras[i]][1]*para_evidencia[letras[i]][2])
    resultado = sum(rel)
    return resultado

def algoritmo_regresion(request):
    bd = list(Post.objects.all())
    """usando solo registros de la letra k"""
    b = Post.objects.filter(num2=bd[0].num2)
    """guradando la columna 1 y 3 los registros de k"""
    col1=[]
    col2=[]
    for i in list(b):
        col1.append(i.num1)
        col2.append(i.num3)
    """calculando b1 y b2"""
    (b1,b2) = cal_regreison(col1,col2)

    if request.method == 'POST':
        x1 = int(request.POST["x"])
        x2 = int(request.POST["y"])
        datos = Post.objects.all()
        b = calcConstante(datos)
        resultado  = valorReferente(datos, x1, x2, b)
        return render(request, 'app1/algoritmo_regresion.html', {'rel': resultado})
    else:
        return render(request, 'app1/algoritmo_regresion.html', {})

def valorReferente(datos, x1, x2, b):
    a1 = 0
    a2 = 0
    caracter = ''
    resp=[]
    for i in list(datos):
        a1 = i.num1
        caracter = i.num2
        a2 = i.num3
        
        salida = 1/(1 + np.exp(-(a1*x1 + a2*x2 + b)))
        if salida > 0.5:
            #respuesta = caracter
            resp.append(caracter)
        else:
            respuesta = f'No hay resultado que haya podido encontrar: {caracter}'
    respuesta = random.choice(resp)
    return respuesta

def calcConstante(datos):
    x = []
    y = []
    xCuadrada = 0
    xy = 0
    for i in list(datos):
        xCuadrada = xCuadrada + i.num1**2
        xy = xy + i.num1 * i.num3
        x.append(i.num1)
        y.append(i.num3)
    xSum = sum(x)
    ySum = sum(y)
    constante = (xCuadrada*ySum - xy*xSum)/(datos.count()*xCuadrada-xSum**2)
    return constante    

def cal_regreison(col1,col2):
    val1=0
    val3=0
    for i in range(len(col1)):
        rel = col1[i]*col2[i]
        val1+=rel

        pos = col1[i]**2
        val3+=pos

    val2 = len(col1)*mean(col1)*mean(col2)
    
    val4 = 1/len(col1)*(sum(col1)**2)

    b1 = (val1 - val2) / (val3 - val4)

    #b2 = (val3 * sum(col2)) - (val1 * sum(col1)) / ((len(col1) * val3) - (sum(col1)**2))

    b2 = mean(col2) - (b1*mean(col1))
    
    return b1,b2