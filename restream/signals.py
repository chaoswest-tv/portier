import logging

from django.dispatch import receiver
from srs.signals import on_publish, on_unpublish

from portier.celery import app as celery

from .models import RestreamConfig
from srs.models import Streamkey

logger = logging.getLogger(__name__)


@receiver(on_unpublish)
def callback_on_unpublish(sender, **kwargs):
    logger.info("stop publish - {}".format(kwargs['name']))
    celery.send_task('main.stop_restream', kwargs={'name': kwargs['name']})


@receiver(on_publish)
def callback_on_publish(sender, **kwargs):
    logger.info("start publish - {}".format(kwargs['name']))
    streamkey = Streamkey.objects.get(key=kwargs['streamkey'])
    configs = RestreamConfig.objects.filter(streamkey=streamkey)
    for config in configs:
        pass
        celery.send_task('main.start_restream', kwargs={
            'app': kwargs['app'],
            'streamkey': kwargs['streamkey'],
            'target': config.target,
            'id': config.id
        })
