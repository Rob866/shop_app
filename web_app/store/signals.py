from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from  django.db.models.signals import  pre_save
from  django.dispatch import receiver
from .models import  ProductoImagen,Basket
from django.contrib.auth.signals import user_logged_in

THUMBNAIL_SIZE = (300, 300)

@receiver(pre_save,sender=ProductoImagen)
def generar_thumbnail(sender,instance,**kwargs):

    imagen = Image.open(instance.imagen)
    imagen = imagen.convert('RGB')
    imagen.thumbnail(THUMBNAIL_SIZE,Image.ANTIALIAS)

    temp_thumb = BytesIO()
    imagen.save(temp_thumb,"JPEG")
    temp_thumb.seek(0)

    instance.thumbnail.save(
                 instance.imagen.name,
                 ContentFile(temp_thumb.read()),
                 save=False,)

    temp_thumb.close()
#mejorar Codigo
@receiver(user_logged_in)
def cargar_basket_si_se_encontro(sender,user,request,**kwargs):
    basket_anonima = getattr(request,"basket",None)
    if basket_anonima:
        try:
            login_basket = Basket.objects.get(user=user,status= Basket.OPEN)

            for basket_item  in basket_anonima.basketitem_set.all():
                add_basket= True
                for login_basket_item in login_basket.basketitem_set.all():
                    if login_basket_item.producto ==  basket_item.producto:
                        add_basket= False
                        login_basket_item.cantidad += basket_item.cantidad
                        login_basket_item.save()
                if add_basket:
                    basket_item.basket = login_basket
                    basket_item.save()

            basket_anonima.delete()
            request.session['basket_id'] = login_basket.id

        except Basket.DoesNotExist:
            basket_anonima.user=user
            basket_anonima.save()
    else:
        try:
            login_basket = Basket.objects.get(user=user,status=Basket.OPEN)
            request.session['basket_id'] = login_basket.id

        except Basket.DoesNotExist:
            print("ACCESO SIN ORDEN CREADA")
