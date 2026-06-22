from django import forms
from .models import Usuario

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Cree una contraseña'}))
    
    class Meta:
        model = Usuario
        fields = ['username', 'correo', 'password', 'rol']
        labels = {
            'username': 'Nombre de Usuario',
            'correo': 'Correo Electrónico',
            'rol': 'Rol del Sistema'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: jhoan'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ej: correo@gmail.com'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario o Correo", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu usuario o correo'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))

class UserEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'correo']
        labels = {
            'username': 'Nombre de Usuario',
            'correo': 'Correo Electrónico',
        }