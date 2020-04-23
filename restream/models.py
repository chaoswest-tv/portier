from django.db import models

# Create your models here.

from rtmp.models import Stream


class RestreamConfig(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    target = models.CharField(max_length=500)
    name = models.CharField(max_length=100)
    active = models.BooleanField()

    def __str__(self):
        return '{} to {}'.format(self.stream, self.name)
