from . import  views
from django.urls import path
app_name= 'store'

urlpatterns = [
    path('',views.ProductListView.as_view(),name='store'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
]
