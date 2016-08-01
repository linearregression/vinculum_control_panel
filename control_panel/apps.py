from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "control_panel"

    def ready(self):
        import_module("control_panel.receivers")
