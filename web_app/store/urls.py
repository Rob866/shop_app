from . import  views
from django.urls import path
from .models import Producto
from django.views.generic.detail import DetailView

app_name= 'store'
urlpatterns = [
    path('',views.ProductListView.as_view(),name='store'),
    path("producto/<slug:slug>/",DetailView.as_view(model=Producto),name="producto_view",),
    path('add_to_order/',views.add_to_basket,name='add_to_order'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('direcciones/',views.DireccionListView.as_view(),name='direcciones'),
    path('direcciones/<int:pk>/',views.DireccionUpdateView.as_view(),name='direccion_update'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/', views.Logout_view.as_view(),name="logout"),
    path('register/',views.Signup_view.as_view(),name='register'),
]
