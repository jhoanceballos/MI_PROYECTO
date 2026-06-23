from django import forms
from .models import Usuario

# ==========================================
# SECCIÓN: FORMULARIO DE REGISTRO DE USUARIOS
# ==========================================
class RegisterForm(forms.ModelForm):
    # Campo de contraseña explícito para usar el widget adecuado en la interfaz
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label="Contraseña"
    )

    class Meta:
        model = Usuario
        # 🛡️ SEGURIDAD: Solo permitimos estos tres campos. El rol se quita de aquí
        # para evitar que usuarios maliciosos se asignen el rol de Administrador.
        fields = ['username', 'correo', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Usuario'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
        }

# ==========================================
# SECCIÓN: FORMULARIO DE INICIO DE SESIÓN
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