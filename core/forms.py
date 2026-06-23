from django import forms
from .models import Usuario
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.forms import EditarPerfilForm
# ==========================================
# SECCIÓN: BASE DE DATOS Y CONEXIÓN DE MODELOS
# ==========================================
# En esta sección mapeamos la estructura de los formularios directamente con 
# nuestro modelo personalizado de base de datos 'Usuario'.

# ==========================================
# SECCIÓN: FORMULARIO DE REGISTRO
# ==========================================
class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label="Contraseña"
    )

    class Meta:
        model = Usuario
        # 🛡️ Solo exponemos campos públicos seguros. El rol se quita para asignarse automáticamente por detrás.
        fields = ['username', 'correo', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Usuario'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
        }

# ==========================================
# SECCIÓN: FORMULARIO DE LOGIN
# ==========================================
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario o Correo'}),
        label="Usuario o Correo"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label="Contraseña"
    )

# ==========================================
# SECCIÓN: FORMULARIO DE PERFIL DE USUARIO
# ==========================================
class UserEditForm(forms.ModelForm):
    """ Formulario encargado de permitir al usuario actualizar sus datos desde su perfil """
    class Meta:
        model = Usuario
        fields = ['username', 'correo']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
        }
# ==========================================
# # SECCIÓN: FORMULARIOS DE PERFIL DE USUARIO
# ==========================================

class EditarPerfilForm(forms.ModelForm):
    """ Formulario para la actualización de datos personales en el perfil """
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'foto_perfil']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control border-2', 'placeholder': 'Tu nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control border-2', 'placeholder': 'Tu apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control border-2', 'placeholder': 'correo@ejemplo.com'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control border-2'}),
        }