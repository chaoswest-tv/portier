from django.dispatch import receiver
from django.db.models.signals import post_save
from rtmp.signals import stream_active
from .models import RestreamConfig
from rtmp.models import Stream
from concierge.models import Task


@receiver(stream_active)
def create_tasks(sender, **kwargs):
    stream = Stream.objects.get(stream=kwargs['stream'])
    instances = RestreamConfig.objects.filter(active=True, stream=stream)
    for instance in instances:
        task = Task(stream=instance.stream, type='restream', config_id=instance.id,
                    configuration=instance.get_json_config())
        task.save()


@receiver(post_save, sender=RestreamConfig)
def update_tasks(sender, **kwargs):
    instance = kwargs['instance']
    # TODO: check for breaking changes using update_fields. This needs custom save_model functions though.

    # Get the current task instance if it exists, and remove it
    try:
        task = Task.objects.filter(config_id=instance.id).get()
        task.delete()
    except Task.DoesNotExist:
        pass

    # If the configuration is set to be active, and the stream is published, (re)create new task
    if instance.active and instance.stream.publish_counter > 0:
        task = Task(stream=instance.stream, type='restream', config_id=instance.id,
                    configuration=instance.get_json_config())
        task.save()
