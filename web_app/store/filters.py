from .models import Producto,ProductoTag
from django import forms
import django_filters

class ProductoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    tags = django_filters.ModelMultipleChoiceFilter(queryset=ProductoTag.objects.all(),widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Producto
        fields = ('nombre','tags')
