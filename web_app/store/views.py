from django.shortcuts import render
from .models import  Producto
# Create your views here.


def store(request):
    productos = Producto.objects.all()
    context = {'productos' : productos}
    return render(request,'store/store.html',context)

def cart(request):
    context = {}
    return render(request,'store/cart.html',context)

def checkout(request):
    context = {}
    return render(request,'store/checkout.html',context)
def home():
    pass

def contact():
    pass

def login():
    pass

def register():
    pass
