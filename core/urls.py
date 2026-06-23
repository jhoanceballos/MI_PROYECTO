"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views

# ==========================================
# # SECCIÓN: RUTAS GLOBALES DEL SISTEMA (URLS)
# ==========================================
urlpatterns = [
    # 🛡️ Extensión nativa del panel de administración de Superusuario
    path('admin/', admin.site.urls),

    # ==========================================
    # # SECCIÓN: AUTENTICACIÓN Y SESIONES (SPA)
    # ==========================================
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # ==========================================
    # # SECCIÓN: VISTAS DE USUARIOS Y PERFILES
    # ==========================================
    path('home/', views.home, name='home'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/editar/', views.editar_profile_view if hasattr(views, 'editar_profile_view') else views.editar_perfil_view, name='editar_perfil'),
    
    # Ruta personalizada para tu propio panel de control de administrador en el menú superior
    path('control/', views.admin_panel_view, name='admin_panel'),
]