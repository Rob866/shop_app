from django.shortcuts import (render,get_object_or_404)
from .models import  (Producto,Order,OrderItem)
from django.views.generic import   (ListView,RedirectView)
from .filters import  ProductoFilter
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import (render,redirect)
from .forms import OrderItemLineFormSet,LoginAutentificationForm,SignUpForm
from django.contrib.auth import login,logout
from django.views.generic.edit import FormView
from django.contrib import  messages


class Signup_view(FormView):
    template_name = "store/register.html"
    form_class = SignUpForm

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return super(Signup_view,self).dispatch(request,*args,**kwargs)

    def get_success_url(self):
        return self.request.GET.get("next", "/")


    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        username = form.cleaned_data.get("username")
        raw_password = form.cleaned_data.get("password1")
        email = form.cleaned_data.get("email")
        nombre = form.cleaned_data.get("nombre")
        email = form.cleaned_data.get("apellido")
        user = authenticate(username=username,password=raw_password,email=email,nombre=nombre,
        apellido= apellido )
        if user is None:
            raise forms.ValidationError('error de autentificación')
        login(self.request, user)
        return response



class LoginView(FormView):
    form_class = LoginAutentificationForm
    template_name = "store/login.html"
    success_url =  '/'

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return super(LoginView,self).dispatch(request,*args,**kwargs)

    def form_valid(self, form):
        login(self.request,form.get_user())
        return super(LoginView, self).form_valid(form)


class Logout_view(RedirectView):
    pattern_name = 'store:store'

    def get(self,request,*args,**kwargs):
        logout(request)
        return super(Logout_view,self).get(request,*args,**kwargs)


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
    if producto:
        messages.success(request, f'Se agrego: { producto.nombre } a tu canasta')

    return HttpResponseRedirect(reverse('store:cart')) 
    #HttpResponseRedirect(reverse('store:producto_view',args=(producto.slug,)))


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

def register(request):
    context = {}
    return render(request,'store/register.html',context)
