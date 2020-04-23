from django.db import models
from django.utils.translation import gettext as _
import uuid

from . import signals


class Application(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text=_("rtmp_application_name"))

    def __str__(self):
        return self.name


class Stream(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    stream = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)

    def on_publish(self, param):
        signals.on_publish.send(sender=self.__class__,
                                name=self.name,
                                stream=self.stream,
                                app=str(self.application),
                                param=param
                                )

    def on_unpublish(self, param):
        signals.on_unpublish.send(sender=self.__class__,
                                  name=self.name,
                                  stream=self.stream,
                                  app=str(self.application),
                                  param=param
                                  )

    def __str__(self):
        return self.name
