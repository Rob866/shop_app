from django.contrib import admin
from store import models
from django.utils.html import format_html


class BasketItemInline(admin.TabularInline):
    model= models.BasketItem
    extra=0

class BasketAdmin(admin.ModelAdmin):
    list_display = ('transaction_id','status',)
    list_filter = ('status',)
    search_fields = ('user__name',)
    inlines = [BasketItemInline,]



class BasketItemAdmin(admin.ModelAdmin):
    list_display = ('producto_nombre_','cantidad',)
    list_filter = ('producto__nombre',)

    def producto_nombre_(self,instance):
        return instance.producto.nombre


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_nombre_',)
    search_fields = ('user__nombre',)

    def user_nombre_(self,instance):
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

admin.site.register(models.Order ,OrderAdmin)
admin.site.register(models.Producto ,ProductoAdmin)
admin.site.register(models.ProductoImagen,ProductoImagenAdmin)
admin.site.register(models.ProductoTag,ProductoTagAdmin)
admin.site.register(models.Basket,BasketAdmin)
admin.site.register(models.BasketItem,BasketItemAdmin)
