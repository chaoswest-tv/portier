from django.dispatch import receiver
from rtmp.signals import stream_active
from .models import RestreamConfig
from rtmp.models import Stream
from concierge.models import Task
import json


@receiver(stream_active)
def create_tasks(sender, **kwargs):
    stream = Stream.objects.get(stream=kwargs['stream'])
    instances = RestreamConfig.objects.filter(active=True, stream=stream)
    for inst in instances:
        config = {
            'name': inst.name,
            'app': inst.stream.application.name,
            'stream': str(inst.stream.stream),
            'target': inst.target
        }

        json_config = json.dumps(config)
        task = Task(stream=stream, type='restream', configuration=json_config)
        task.save()
