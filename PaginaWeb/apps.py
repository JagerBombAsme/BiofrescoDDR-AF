from django.apps import AppConfig

class PaginawebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PaginaWeb'

    def ready(self):
        import PaginaWeb.signals
