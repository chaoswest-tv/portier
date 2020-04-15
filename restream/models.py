from django.db import models

# Create your models here.

from srs.models import Application, Streamkey

class RestreamConfig(models.Model):
    streamkey = models.ForeignKey(Streamkey, on_delete=models.CASCADE)
    target = models.CharField(max_length=500)
    name = models.CharField(max_length=100)
    active = models.BooleanField()

    def __str__(self):
        return '{} to {}'.format(self.streamkey, self.name)
