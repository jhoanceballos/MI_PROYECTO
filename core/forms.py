from django import forms
from .models import Usuario

# ==========================================
# # SECCIÓN: FORMULARIOS DEL SISTEMA SAFEZONE
# ==========================================

class RegisterForm(forms.ModelForm):
    """ Formulario base para el registro de nuevos usuarios """
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    """ Formulario para la autenticación de usuarios """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario o Correo'}),
        label="Usuario o Correo"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label="Contraseña"
    )

class UserEditForm(forms.ModelForm):
    """ Formulario genérico de edición rápida """
    class Meta:
        model = Usuario
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class EditarPerfilForm(forms.ModelForm):
    """ Formulario completo para actualizar nombres, apellidos, correo y foto """
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'foto_perfil']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control border-2', 'placeholder': 'Tu nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control border-2', 'placeholder': 'Tu apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control border-2', 'placeholder': 'correo@ejemplo.com'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control border-2'}),
        }