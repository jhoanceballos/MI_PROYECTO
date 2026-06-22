from django.http import HttpResponseForbidden

def admin_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        # Verifica si está autenticado y si es Administrador
        if request.user.is_authenticated and request.user.rol and request.user.rol.nombre == 'Administrador':
            return view_func(request, *args, **kwargs)
        else:
            # Si no es admin, le deniega el acceso con un error 403
            return HttpResponseForbidden("No tienes permisos para acceder a esta sección.")
    return _wrapped_view_func