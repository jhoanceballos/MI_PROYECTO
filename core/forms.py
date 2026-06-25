from django import forms
from .models import Usuario

# ==========================================
# SECCIÓN: FORMULARIO DE REGISTRO
# ==========================================
class RegisterForm(forms.ModelForm):
    """ Formulario base para el registro de nuevos usuarios en SafeZone """
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'correo']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre de usuario'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Contraseña'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'correo@ejemplo.com'
            }),
        }

# ==========================================
# SECCIÓN: FORMULARIO DE AUTENTICACIÓN (LOGIN)
# ==========================================
class LoginForm(forms.Form):
    """ Formulario para la autenticación de usuarios mediante username o correo """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Usuario o Correo'
        }),
        label="Usuario o Correo"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Contraseña'
        }),
        label="Contraseña"
    )

# ==========================================
# SECCIÓN: FORMULARIO DE CONFIGURACIÓN DE PERFIL
# ==========================================
class EditarPerfilForm(forms.ModelForm):
    """ Formulario unificado para la actualización de datos personales en la interfaz de perfil """
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'correo', 'foto_perfil']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control border-2', 
                'placeholder': 'Tu nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control border-2', 
                'placeholder': 'Tu apellido'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control border-2', 
                'placeholder': 'correo@ejemplo.com'
            }),
            'foto_perfil': forms.FileInput(attrs={
                'class': 'form-control border-2'
            }),
        }