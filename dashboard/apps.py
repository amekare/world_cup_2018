from django.apps import AppConfig


class MundialConfig(AppConfig):
    name = 'dashboard'

    def ready(self):
        from . import signals