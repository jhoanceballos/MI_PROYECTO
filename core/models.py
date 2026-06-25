from django.db import models
from django.contrib.auth.models import AbstractUser

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    correo = models.EmailField(unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    
    # CORRECCIÓN: Se cambió 'upload_dir' por 'upload_to'
    foto_perfil = models.ImageField(
        upload_to='perfiles/', 
        null=True, 
        blank=True, 
        default='perfiles/default.png'
    )

    def __str__(self):
        return self.username