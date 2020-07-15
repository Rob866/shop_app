from django.db import models
from django.core.validators import  MinValueValidator
from django.contrib.auth.models import User
from django.contrib import admin



class ProductoTag(models.Model):
    nombre = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48)
    descripcion = models.TextField('descripción')
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name=('Tag')
        verbose_name_plural=('Tags')

    def __str__(self):
        return self.nombre



class Producto(models.Model):
    nombre = models.CharField(max_length=60)
    tags = models.ManyToManyField(ProductoTag,blank=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField('Precio',max_digits=6,decimal_places=2)
    slug = models.SlugField(max_length=48)
    activo = models.BooleanField(default=True)
    en_stock = models.BooleanField(default=True)
    actualizacion = models.DateTimeField(auto_now=True)


    class Meta:
        ordering=('nombre',)
        verbose_name_plural=('Productos')

    def __str__(self):
        return self.nombre


class ProductoImagen(models.Model):
    producto = models.ForeignKey(
                Producto,
                on_delete= models.CASCADE,
                related_name="imagenes")

    imagen = models.ImageField(upload_to='imagenes-del-producto')
    thumbnail =  models.ImageField(upload_to='producto-thumbnails',null=True,blank=True)

    class Meta:
        verbose_name = ('Imagen de Producto')
        verbose_name_plural=('Imagenes de Productos')



class Order(models.Model):
    OPEN = 0
    SUBMITTED = 1
    STATUSES= ((OPEN, 'Abierto'),(SUBMITTED,'Completado'))
    status =  models.IntegerField(choices=STATUSES, default=OPEN)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100,null=True)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    @property
    def is_empty(self):
        return self.orderitem_set.all().count() == 0

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.cantidad for item in orderitems])
        return total



class OrderItem(models.Model):
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    cantidad = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)])
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.producto.precio * self.cantidad
        return total



class ShippingAddress(models.Model):
    PAISES_SOPORTADOS = (
       ('mx','Mexico'),
       ('eu','EUA'))
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    direccion = models.CharField(max_length=200, null=False)
    ciudad = models.CharField(max_length=200, null=False)
    estado = models.CharField(max_length=200, null=False)
    zipcode = models.CharField('Codigo postal',max_length=200, null=False)
    pais = models.CharField(max_length=3,choices=PAISES_SOPORTADOS)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.direccion
