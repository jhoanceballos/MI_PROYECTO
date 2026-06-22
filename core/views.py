def inicio(request):
    if request.user.is_authenticated:
        # Si ya está logueado, evaluamos su rol para saber a dónde mandarlo
        if request.user.rol and request.user.rol.nombre == 'Administrador':
            return redirect('admin_dashboard')  # Reemplaza con el nombre de tu URL de admin
        return redirect('home')
    return redirect('login')
@login_required(login_url='login')
@admin_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')
def login_view(request):
    if request.user.is_authenticated:
        if request.user.rol and request.user.rol.nombre == 'Administrador':
            return redirect('admin_dashboard')
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
                
                # 🚀 AQUÍ SE APLICA LA MAGIA DEL ROL:
                # Comprobamos si el usuario tiene asignado el rol de "Administrador"
                # (Ajusta 'Administrador' según cómo se guarde textualmente en tu base de datos)
                if user.rol and user.rol.nombre == 'Administrador':
                    messages.success(request, f'¡Bienvenido Administrador {user.username}!')
                    return redirect('admin_dashboard') # Tu vista de admin
                
                messages.success(request, f'¡Bienvenido {user.username}!')
                return redirect('home') # Tu vista de usuario común
            else:
                messages.error(request, 'Usuario, correo o contraseña incorrectos.')
        else:
            print("Errores en el login:", form.errors)
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})