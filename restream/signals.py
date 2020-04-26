from django.dispatch import receiver
from rtmp.signals import stream_active
from .models import RestreamConfig
from rtmp.models import Stream
from concierge.models import Task


@receiver(stream_active)
def create_tasks(sender, **kwargs):
    stream = Stream.objects.get(stream=kwargs['stream'])
    configs = RestreamConfig.objects.filter(stream=stream)
    for config in configs:
        task = Task(stream=stream, type='restream', configuration='{}')
        task.save()
