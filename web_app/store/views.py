from django.shortcuts import render
from .models import  Producto
from django.views.generic.list import ListView
from .filters import  ProductoFilter

class ProductListView(ListView):
    model = Producto
    template_name= 'store/store.html'
    paginate_by = 2

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductoFilter(self.request.GET,queryset=self.get_queryset())
        return context

def cart(request):
    context = {}
    return render(request,'store/cart.html',context)


def checkout(request):
    context = {}
    return render(request,'store/checkout.html',context)
