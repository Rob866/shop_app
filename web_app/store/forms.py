from  django.forms import inlineformset_factory
from .models import  Basket,BasketItem,Direccion
from django.contrib.auth import authenticate,get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields=('username','password1', 'password2','email','nombre','apellido')


class LoginAutentificationForm(forms.Form):
    username= forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self,request=None,*args,**kwargs):
        self.request = request
        self.user = None
        super(LoginAutentificationForm,self).__init__(*args,**kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user = authenticate(username=username,password=password)
        if self.user is None:
            raise forms.ValidationError('error de autentificación')
        return self.cleaned_data

    def get_user(self):
        return self.user


BasketItemLineFormSet = inlineformset_factory(
 Basket
,BasketItem
,fields=('cantidad',)
,extra=0,)


class UpdateViewForm(forms.ModelForm):
    PAISES_SOPORTADOS = (('mx','Mexico'),('eu','EUA'))
    pais = forms.ChoiceField(choices=PAISES_SOPORTADOS,widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Direccion
        fields =('direccion1', 'direccion2','zip_code','estado','ciudad','pais')
