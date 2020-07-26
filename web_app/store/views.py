from django.shortcuts import (render,get_object_or_404)
from .models import  (Producto,Basket,BasketItem,Direccion)
from django.views.generic import   (ListView,RedirectView,UpdateView)
from .filters import  ProductoFilter
from django.http import  HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import (render,redirect)
from .forms import BasketItemLineFormSet,LoginAutentificationForm,SignUpForm,UpdateViewForm
from django.contrib.auth import login,logout
from django.views.generic.edit import FormView
from django.contrib import  messages
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin



class DireccionListView(LoginRequiredMixin,ListView):
    model = Direccion
    template_name = "store/direccion_list.html"
    context_object_name = 'direcciones'

    def get_queryset(self):
        queryset = super(DireccionListView,self).get_queryset()
        return queryset.filter(customer=self.request.user)


class DireccionUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "store/direccion_update.html"
    model = Direccion
    form_class = UpdateViewForm

    success_url = reverse_lazy("store:direcciones")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(customer= self.request.user)




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
        apellido = form.cleaned_data.get("apellido")
        user = authenticate(username=username,password=raw_password,email=email,nombre=nombre,
        apellido=apellido)
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


def add_to_basket(request):
    producto = get_object_or_404(Producto,pk=request.GET.get('product_id'))
    basket = request.basket

    if not request.basket:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        basket = Basket.objects.create(user=user)
        request.session['basket_id'] = basket.id
    basketItem,created  = BasketItem.objects.get_or_create(basket=basket,producto=producto)

    if not created:
        basketItem.cantidad += 1
        basketItem.save()
    if producto:
        messages.success(request, f'Se agrego: { producto.nombre } a tu canasta')

    return HttpResponseRedirect(reverse('store:cart'))
    #HttpResponseRedirect(reverse('store:producto_view',args=(producto.slug,)))


def cart(request):
    if not request.basket:
        return render(request,'store/cart.html',{ 'formset': None})

    if request.method == 'POST':
        formset = BasketItemLineFormSet(request.POST,instance=request.basket)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('store:cart'))
    else:
        formset = BasketItemLineFormSet(instance=request.basket)

    if request.basket.is_empty:
        return render(request,'store/cart.html',{ 'formset': None})

    return render(request,'store/cart.html',{ 'formset': formset})


def checkout(request):
    context = {}
    return render(request,'store/checkout.html',context)
