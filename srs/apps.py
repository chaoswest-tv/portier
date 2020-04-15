from django.apps import AppConfig


class SrsConfig(AppConfig):
    name = 'srs'

    def ready(self):
        import srs.signals  #noqa
