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
from django.urls import path
from . import views

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),
    
    # Ruta raíz redirige automáticamente
    path('', views.inicio, name='inicio'),
    
    # Autenticación con rutas exclusivas
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Vistas de la aplicación protegidas
    path('home/', views.home, name='home'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/editar/', views.editar_perfil_view, name='editar_perfil'),
]
