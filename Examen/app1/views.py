from django.shortcuts import render
from .models import Post

# Create your views here.
def suma(val):
    return print(val)
def post_list(request):
    consulta = Post.objects.all()
    cont = {'datos':consulta}
    return render(request, 'app1/post_list.html', cont, function=suma(5))