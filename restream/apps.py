from django.apps import AppConfig


class RestreamConfig(AppConfig):
    name = 'restream'

    def ready(self):
        import restream.signals  # noqa
