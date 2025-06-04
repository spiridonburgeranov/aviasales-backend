from django.apps import AppConfig


class AirlanseBookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'airlanse_book'

    def ready(self):
        from . import signals