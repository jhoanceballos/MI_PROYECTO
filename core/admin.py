from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol

# ==========================================
# # SECCIÓN: GESTIÓN DE ROLES EN EL PANEL
# ==========================================
@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']

# ==========================================
# # SECCIÓN: GESTIÓN DE USUARIOS EN EL PANEL
# ==========================================
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuración del panel de administración para el modelo Usuario.
    Mapea de forma segura los atributos nativos de AbstractUser.
    """
    # 📝 CORRECCIÓN: Usamos 'is_active' en lugar de 'estado' y 'date_joined' en lugar de 'fecha_registro'
    list_display = ['id', 'username', 'correo', 'rol', 'is_active', 'date_joined']
    
    # Filtros laterales del panel
    list_filter = ['rol', 'is_active']
    
    # Criterios de búsqueda rápida
    search_fields = ['username', 'correo']
    
    # Orden predeterminado en la tabla
    ordering = ['id']

    # ==========================================
    # # SECCIÓN: CONFIGURACIÓN DE FORMULARIOS ADMIN
    # ==========================================
    # Desplegamos el campo personalizado 'rol' dentro del formulario de edición del Admin
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Permisos del Sistema', {'fields': ('rol',)}),
    )
    
    # Desplegamos el campo 'rol' al crear un usuario desde el panel
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información de Permisos del Sistema', {'fields': ('rol',)}),
    )