from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponseForbidden

from .models import Usuario, Rol
from .forms import RegisterForm, LoginForm, EditarPerfilForm

def admin_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.rol and request.user.rol.nombre == 'Administrador':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("No tienes permisos para acceder a esta sección.")
    return _wrapped_view_func

def inicio(request):
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            input_usuario = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            username_final = input_usuario
            if '@' in input_usuario:
                try:
                    usuario_db = Usuario.objects.get(correo=input_usuario)
                    username_final = usuario_db.username
                except Usuario.DoesNotExist:
                    pass

            user = authenticate(request, username=username_final, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'¡Bienvenido {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Usuario, correo o contraseña incorrectos.')
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            correo = form.cleaned_data.get('correo')
            password = form.cleaned_data.get('password')
            
            rol_por_defecto, created = Rol.objects.get_or_create(nombre='Usuario Común')
            
            user = Usuario(username=username, correo=correo, rol=rol_por_defecto)
            user.set_password(password)
            user.save()
            
            messages.success(request, '¡Registro exitoso! Ya puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Hubo un error en el registro. Verifica los campos.')
    else:
        form = RegisterForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
@never_cache
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def perfil_view(request):
    usuario = request.user
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu perfil ha sido actualizado con éxito!")
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=usuario)
        
    return render(request, 'perfil.html', {'form': form, 'usuario': usuario})

@login_required(login_url='login')
@never_cache
@admin_required
def admin_panel_view(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        rol_id = request.POST.get('rol_id')
        
        usuario_editar = get_object_or_404(Usuario, id=usuario_id)
        nuevo_rol = get_object_or_404(Rol, id=rol_id)
        
        usuario_editar.rol = nuevo_rol
        usuario_editar.save()
        
        messages.success(request, f"El rol de {usuario_editar.username} ha sido actualizado.")
        return redirect('admin_panel')
        
    context = {
        'usuarios': Usuario.objects.all().select_related('rol').order_by('id'),
        'roles': Rol.objects.all()
    }
    return render(request, 'admin_panel.html', context)