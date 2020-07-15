from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from  django.db.models.signals import  pre_save
from  django.dispatch import receiver
from .models import  ProductoImagen,Order
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
#apesta
@receiver(user_logged_in)
def cargar_ordenes_si_se_encontraron(sender,user,request,**kwargs):
    order_anonima = getattr(request,"order",None)
    if order_anonima:
        try:
            login_order = Order.objects.get(user=user,status=Order.OPEN)

            for order_item  in order_anonima.orderitem_set.all():
                add_order= True
                for login_order_item in login_order.orderitem_set.all():
                    if login_order_item.producto ==  order_item.producto:
                        add_order= False
                        login_order_item.cantidad += order_item.cantidad
                        login_order_item.save()
                if add_order:
                    order_item.order = login_order
                    order_item.save()

            order_anonima.delete()
            request.session['order_id'] = login_order.id

        except Order.DoesNotExist:
            order_anonima.user=user
            order_anonima.save()
    else:
        try:
            login_order = Order.objects.get(user=user,status=Order.OPEN)
            request.session['order_id'] = login_order.id

        except Order.DoesNotExist:
            print("ACCESO SIN ORDEN CREADA")
