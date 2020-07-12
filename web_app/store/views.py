from django.shortcuts import (render,get_object_or_404)
from .models import  (Producto,Order,OrderItem)
from django.views.generic.list import ListView
from .filters import  ProductoFilter
from django.http import  HttpResponseRedirect
from django.urls import reverse
from .forms import OrderItemLineFormSet

class ProductListView(ListView):
    model = Producto
    template_name= 'store/store.html'
    paginate_by = 2

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductoFilter(self.request.GET,queryset=self.get_queryset())
        return context


def add_to_order(request):
    producto = get_object_or_404(Producto,pk=request.GET.get('product_id'))
    order = request.order

    if not request.order:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        order = Order.objects.create(user=user)
        request.session['order_id'] = order.id
    orderItem,created  = OrderItem.objects.get_or_create(order=order,producto=producto)

    if not created:
        orderItem.cantidad += 1
        orderItem.save()
    return HttpResponseRedirect(reverse('store:producto_view',args=(producto.slug,)))

def cart(request):
    if not request.order:
        return render(request,'store/cart.html',{ 'formset': None})

    if request.method == 'POST':
        formset = OrderItemLineFormSet(request.POST,instance=request.order)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('store:cart'))
    else:
        formset = OrderItemLineFormSet(instance=request.order)

    if request.order.is_empty:
        return render(request,'store/cart.html',{ 'formset': None})

    return render(request,'store/cart.html',{ 'formset': formset})




def checkout(request):
    context = {}
    return render(request,'store/checkout.html',context)
