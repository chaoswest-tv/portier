import logging

from django.dispatch import receiver
from rtmp.signals import on_publish, on_unpublish

from portier.celery import app as celery

from .models import RestreamConfig
from rtmp.models import Stream

logger = logging.getLogger(__name__)


@receiver(on_unpublish)
def callback_on_unpublish(sender, **kwargs):
    logger.info("stop publish - {}".format(kwargs['name']))
    celery.send_task('main.stop_restream', kwargs={'name': kwargs['name']})


@receiver(on_publish)
def callback_on_publish(sender, **kwargs):
    logger.info("start publish - {}".format(kwargs['name']))
    stream = Stream.objects.get(key=kwargs['stream'])
    configs = RestreamConfig.objects.filter(stream=stream)
    for config in configs:
        celery.send_task('main.start_restream', kwargs={
            'app': kwargs['app'],
            'stream': kwargs['stream'],
            'target': config.target,
            'id': config.id
        })
