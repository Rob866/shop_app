from django.contrib import admin
from store import models
from django.utils.html import format_html

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('nombre','email',)
    list_filter = ('nombre','email',)
    search_fields = ('nombre','email')


class OrderItemInline(admin.TabularInline):
    model= models.OrderItem
    extra=0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_nombre_','transaction_id','complete',)
    list_filter = ('complete',)
    search_fields = ('customer__nombre',)
    inlines = [OrderItemInline,]

    def customer_nombre_(self,instance):
        return instance.customer.nombre

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('producto_nombre_','cantidad',)
    list_filter = ('producto__nombre',)

    def producto_nombre_(self,instance):
        return instance.producto.nombre


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('customer_nombre_',)
    search_fields = ('customer__nombre',)

    def customer_nombre_(self,instance):
        return instance.customer.nombre



class ProductoImagenInline(admin.TabularInline):
    model= models.ProductoImagen
    extra=0

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre','slug','en_stock','precio',)
    list_filter = ('activo','en_stock','actualizacion',)
    list_editable = ('en_stock',)
    prepopulated_fields = {"slug": ("nombre",)}
    autocomplete_fields = ('tags',)
    search_fields = ('nombre',)
    inlines = [ProductoImagenInline,]

class ProductoImagenAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_tag','producto_nombre',)
    readonly_fields = ('thumbnail',)
    search_fields = ('producto__nombre',)


    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="%s"/>' % obj.thumbnail.url
            )
        return "-"
    thumbnail_tag.short_description = "Thumbnail"

    def producto_nombre(self, obj):
        return obj.producto.nombre


class ProductoTagAdmin(admin.ModelAdmin):

    list_display = ('nombre','descripcion', 'slug')
    list_filter = ('activo',)
    search_fields = ('nombre',)
    prepopulated_fields = {"slug": ("nombre",)}
    #autocomplete_fields = ('productos',)

admin.site.register(models.ShippingAddress ,ShippingAddressAdmin)
admin.site.register(models.Producto ,ProductoAdmin)
admin.site.register(models.ProductoImagen,ProductoImagenAdmin)
admin.site.register(models.ProductoTag,ProductoTagAdmin)
admin.site.register(models.Customer,CustomerAdmin)
admin.site.register(models.Order,OrderAdmin)
admin.site.register(models.OrderItem,OrderItemAdmin)
