from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

#User model configuration
class UserManager(BaseUserManager):

    def create_user(self,username,email,nombre,apellido,password=None):
        if not username:
            raise ValueError('Username no puede estar en blanco')
        if not email:
            raise ValueError('El correo electrónico no puede dejarse en blanco.')
        if not nombre:
            raise ValueError('El Nombre no puede estar en blanco')
        if not apellido:
            raise ValueError('El Apellido electrónico no puede dejarse en blanco.')

        email= self.normalize_email(email)
        user = self.model(username=username,email=email,nombre=nombre,apellido=apellido)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,email,nombre,apellido,password):
        user = self.create_user(
                    username=username,
                    email=email,
                    nombre=nombre,
                    apellido=apellido,
                    password=password)

        user.is_staff = True
        user.is_admin = True
        user.is_superuser= True
        user.save(using=self._db)
        return user



class Usuario(AbstractBaseUser,PermissionsMixin):
        username =  models.CharField(max_length=30,unique=True)
        email   =  models.EmailField(max_length=60,unique=True)
        nombre = models.CharField(max_length=100)
        apellido = models.CharField(max_length=100)


        USERNAME_FIELD  = 'username'
        REQUIRED_FIELDS = ['email','nombre','apellido']

        objects = UserManager()

        date_joined  =  models.DateTimeField(verbose_name="Fecha de ingreso",auto_now_add=True)
        last_login   =  models.DateTimeField(verbose_name="Ultima fecha de Sesión",auto_now=True)
        is_admin     =  models.BooleanField(verbose_name="¿Es Administrador?",default=False)
        is_active    =  models.BooleanField(verbose_name="¿Esta Acivo?",default=True)
        is_staff     =  models.BooleanField(verbose_name="¿Es parte del Staff?",default=False)
        is_superuser =  models.BooleanField(verbose_name="¿Es Super Usuario?",default=False)

        def  __str__(self):
            return f'{self.nombre}'

        def has_perm(self,perm,obj=None):
            return self.is_admin


        def has_module_perms(self,app_label):
            return True
