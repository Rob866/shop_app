from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from  django.db.models.signals import  pre_save
from  django.dispatch import receiver
from .models import  ProductoImagen


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
