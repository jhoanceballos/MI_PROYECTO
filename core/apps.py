from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Fuerza a Django a registrar el archivo admin cuando la app esté lista
        import core.admin
