from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from django.contrib.auth.models import User
        from django.db.models.signals import post_save
        from portier.common import handlers
        post_save.connect(handlers.add_to_default_group, sender=User)
