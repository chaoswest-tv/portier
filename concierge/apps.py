from django.apps import AppConfig


class ConciergeConfig(AppConfig):
    name = 'concierge'

    def ready(self):
        import concierge.signals  # noqa
