from django.apps import AppConfig


class RtmpConfig(AppConfig):
    name = 'rtmp'

    def ready(self):
        import rtmp.signals  # noqa
