from django.contrib import admin
from core.models import Rol, Usuario

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    # Configura las columnas que se verán en la lista
    list_display = ('id', 'nombre')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # Muestra los datos clave del usuario en forma de tabla
    list_display = ('id', 'username', 'correo', 'rol', 'estado', 'fecha_registro')
    # Añade un filtro lateral por rol y estado
    list_filter = ('rol', 'estado')