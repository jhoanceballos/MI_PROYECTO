from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse, HttpResponseForbidden
from .forms import RegisterForm, LoginForm, UserEditForm
from .models import Usuario, Rol  # Importamos Rol para la asignación automática

# ==========================================
# SECCIÓN: DECORADORES Y RESTRICCIONES DE ACCESO
# ==========================================
def admin_required(view_func):
    """ Restringe el acceso a vistas solo para usuarios con rol Administrador """
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.rol and request.user.rol.nombre == 'Administrador':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("No tienes permisos para acceder a esta sección.")
    return _wrapped_view_func

# ==========================================
# SECCIÓN: ENRUTAMIENTO INICIAL (INDEX)
# ==========================================
def inicio(request):
    """ Evalúa si el usuario está logueado y lo redirige según corresponda """
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('login')

# ==========================================
# SECCIÓN: GESTIÓN DE AUTENTICACIÓN (REGISTRO, LOGIN, LOGOUT)
# ==========================================
def register_view(request):
    """ Procesa el formulario de registro de nuevos usuarios sin selección manual de rol """
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            correo = form.cleaned_data.get('correo')
            password = form.cleaned_data.get('password')
            
            # 🛡️ ASIGNACIÓN AUTOMÁTICA DE ROL POR SEGURIDAD
            # Busca el rol 'Usuario Común'. Si por alguna razón no existe en tu BD, lo crea.
            rol_por_defecto, created = Rol.objects.get_or_create(nombre='Usuario Común')
            
            # Solución al AttributeError: Instanciamos el objeto directamente
            user = Usuario(
                username=username,
                correo=correo,
                rol=rol_por_defecto
            )
            # Encriptamos la contraseña de manera segura antes de guardar
            user.set_password(password)
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
    """ Gestiona el inicio de sesión permitiendo tanto el Username como el Correo electrónico """
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            input_usuario = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            username_final = input_usuario
            # Si el usuario ingresó un correo (@), buscamos su username real correspondiente
            if '@' in input_usuario:
                try:
                    usuario_db = Usuario.objects.get(correo=input_usuario)
                    username_final = usuario_db.username
                except Usuario.DoesNotExist:
                    pass

            # Autenticación oficial con las herramientas de Django
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
    """ Cierra la sesión activa y redirige al Login """
    auth_logout(request)
    return redirect('login')

# ==========================================
# SECCIÓN: VISTAS DE NAVEGACIÓN Y PERFIL DE USUARIO
# ==========================================
@login_required(login_url='login')
@never_cache
def home(request):
    """ Renderiza la página principal del ecosistema """
    return render(request, 'home.html')

@login_required(login_url='login')
@never_cache
def perfil_view(request):
    """ Carga la vista del perfil del usuario logueado con su formulario de edición """
    usuario_actual = request.user
    form = UserEditForm(instance=usuario_actual)
    return render(request, 'perfil.html', {'usuario': usuario_actual, 'form': form})[cite: 5]

@login_required(login_url='login')
@never_cache
def editar_perfil_view(request):
    """ Procesa la actualización de los datos del perfil mediante peticiones AJAX """
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