from django.dispatch import receiver
from rtmp.signals import stream_inactive
from .models import Task
from rtmp.models import Stream


@receiver(stream_inactive)
def delete_tasks(sender, **kwargs):
    # when a stream was unpublished, all related tasks need to be deleted.
    stream = Stream.objects.get(stream=kwargs['stream'])
    Task.objects.filter(stream=stream).delete()
