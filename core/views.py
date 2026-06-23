from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse, HttpResponseForbidden
from .forms import RegisterForm, LoginForm, UserEditForm
from .models import Usuario

def admin_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.rol and request.user.rol.nombre == 'Administrador':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("No tienes permisos para acceder a esta sección.")
    return _wrapped_view_func

def inicio(request):
    if request.user.is_authenticated:
        if request.user.rol and request.user.rol.nombre == 'Administrador':
            return redirect('home')  # Redirige temporalmente a home o tu vista panel admin
        return redirect('home')
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
            rol = form.cleaned_data.get('rol')
            
            user = Usuario.objects.create_user(
                username=username,
                correo=correo,
                password=password,
                rol=rol
            )
            user.save()
            messages.success(request, '¡Registro exitoso! Ya puedes iniciar sesión.')
            return redirect('login')
        else:
            print("Errores en el registro:", form.errors)
            messages.error(request, 'Hubo un error en el registro. Verifica los campos.')
    else:
        form = RegisterForm()
    return render(request, 'login.html', {'form': form})

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
            print("Errores en el login:", form.errors)
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url='login')
@never_cache
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
@never_cache
def perfil_view(request):
    usuario_actual = request.user
    form = UserEditForm(instance=usuario_actual)
    return render(request, 'perfil.html', {'usuario': usuario_actual, 'form': form})

@login_required(login_url='login')
@never_cache
def editar_perfil_view(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success', 
                'message': '¡Tu información de perfil ha sido actualizada con éxito!'
            })
        else:
            error_msg = "Error en los datos."
            for field, errors in form.errors.items():
                error_msg = errors[0]
                break
            return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Petición no permitida.'}, status=400)