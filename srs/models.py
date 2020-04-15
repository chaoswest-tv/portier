from django.db import models
from django.conf import settings
import uuid

from . import signals

class Application(models.Model):
    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name


class Streamkey(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    key = models.CharField(max_length=64, unique=True, default=uuid.uuid4())
    name = models.CharField(max_length=100)

    def on_publish(self, client_ip, client_id, vhost, param):
        signals.on_publish.send(sender=self.__class__,
                                name=self.name,
                                streamkey=self.key,
                                app=str(self.application),
                                client_ip=client_ip,
                                client_id=client_id,
                                vhost=vhost,
                                param=param
                                )

    def on_unpublish(self, client_ip, client_id, vhost, param):
        signals.on_unpublish.send(sender=self.__class__,
                                name=self.name,
                                streamkey=self.key,
                                app=str(self.application),
                                client_ip=client_ip,
                                client_id=client_id,
                                vhost=vhost,
                                param=param
                                )

    def __str__(self):
        return '{}'.format(self.name)
