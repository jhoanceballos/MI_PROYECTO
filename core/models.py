from django.db import models
from django.contrib.auth.models import AbstractUser

# ==========================================
# # SECCIÓN: ESTRUCTURA DE ROLES (BASE DE DATOS)
# ==========================================
class Rol(models.Model):
    # 📝 Corrección: Se cambió 'max_index=True' por 'db_index=True'
    nombre = models.CharField(db_index=True, max_length=50, unique=True)

    def __str__(self):
        return self.nombre

# ==========================================
# # SECCIÓN: BASE DE DATOS DE USUARIOS
# ==========================================
class Usuario(AbstractUser):
    """
    Modelo personalizado que extiende de AbstractUser para heredar la 
    infraestructura nativa de autenticación y encriptación de Django.
    """
    correo = models.EmailField(unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)

    # El correo se añade como campo requerido alternativo al crear superusuarios
    REQUIRED_FIELDS = ['correo']

    def __str__(self):
        return self.username