from django import forms
from .models import Usuario

class RegisterForm(forms.ModelForm):
    """
    Formulario para el registro de nuevos usuarios en la plataforma SafeZone.
    
    Utiliza un mapeo directo sobre el modelo 'Usuario' (ModelForm) para gestionar
    las credenciales básicas de acceso y contacto.
    
    Capas de Seguridad:
    - Validación implícita contra inyección SQL mediante el uso de campos tipados de Django.
    - El widget 'PasswordInput' oculta los caracteres de la contraseña en la interfaz.
    """
    class Meta:
        model = Usuario
        # Campos del modelo expuestos de forma estricta en el formulario
        fields = ['username', 'password', 'correo']
        
        # Inyección de clases CSS de Bootstrap para el diseño e interactividad responsiva
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


class LoginForm(forms.Form):
    """
    Formulario estándar para la autenticación de usuarios.
    
    A diferencia de un ModelForm, hereda de 'forms.Form' debido a que implementa 
    una lógica de negocio flexible: el campo 'username' acepta de forma indistinta 
    tanto el nombre de usuario (string) como el correo electrónico (evaluado 
    posteriormente en la vista mediante expresiones regulares).
    """
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


class EditarPerfilForm(forms.ModelForm):
    """
    Formulario para la actualización y gestión de los datos de perfil de usuario.
    
    Soporta la modificación de campos del core de autenticación y gestiona
    el procesamiento multimedia para la carga del archivo de imagen de perfil.
    
    Mecanismos de Protección:
    - Vinculado al parámetro 'enctype="multipart/form-data"' en el cliente para
      garantizar un flujo binario seguro del archivo hacia el backend.
    """
    class Meta:
        model = Usuario
        # Campos permitidos para edición del perfil de usuario común o administrador
        fields = ['first_name', 'last_name', 'correo', 'foto_perfil']
        
        # Estilos aplicados con Bootstrap utilizando bordes definidos (border-2) para la interfaz
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