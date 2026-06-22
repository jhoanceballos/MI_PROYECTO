from django.db import models

class Rol(models.Model):
    """Tabla para almacenar los roles del sistema (Admin, Cliente, etc.)"""
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    """Tabla personalizada para la gestión de usuarios"""
    username = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)  # Guardará la contraseña encriptada
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)  # True = Activo, False = Inactivo
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)  # <-- AQUÍ SE CORRIGIÓ

    def __str__(self):
        return self.username