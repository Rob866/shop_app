from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm,ReadOnlyPasswordHashField


class CustomUserChangeForm(UserChangeForm):

    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("Las contraseñas sin procesar no se almacenan, por lo que no hay forma de ver la contraseña de este usuario, "
                    "pero puede cambiar la contraseña mediante este formulario."
                    "<a href=\"../password/\">formulario</a>."))
    class Meta:
        model = models.Usuario
        fields = '__all__'


@admin.register(models.Usuario)
class UserAdmin(UserAdmin):
    form = CustomUserChangeForm
    fieldsets = (
        ("Credenciales", {"fields": ("username", "password")}),
        (
            "Información Personal",
            {"fields": ("nombre", "apellido",'email')},
        ),
        (
            "Permisos",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_admin",
                             "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Fechas importantes",
            {"fields": ("last_login", "date_joined")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("nombre","apellido","email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "username",
        "nombre",
        "apellido",
        "email",
        "is_staff",
    )
    readonly_fields = ['date_joined','last_login',]
    search_fields = ("email", "nombre", "apellido")
    ordering = ("username",)
