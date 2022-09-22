from django.apps import AppConfig


class AldyseappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aldyseApp'

    def ready(self):
        from . import updater
        updater.start()

