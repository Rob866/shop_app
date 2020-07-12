from  django.forms import inlineformset_factory
from .models import  Order,OrderItem


OrderItemLineFormSet = inlineformset_factory(Order,OrderItem,fields=('cantidad',),extra=0,)
