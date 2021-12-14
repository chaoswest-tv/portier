from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete
from portier.common import handlers
import json

from rtmp.models import Stream


class RestreamConfig(models.Model):
    FORMATS = (
        ('flv', 'flv (RTMP)'),
        ('mpegts', 'mpegts (SRT)'),
    )
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, help_text=_('restreamconfig_stream_help'))
    target = models.CharField(max_length=500, help_text=_('restreamconfig_target_help'))
    name = models.CharField(max_length=100, help_text=_('restreamconfig_name_help'))
    active = models.BooleanField(help_text=_('restreamconfig_activate_help'))
    format = models.CharField(max_length=6, choices=FORMATS, default='flv', help_text=_('restreamconfig_format_help'))

    class Meta:
        verbose_name = _('restreamconfig_verbose_name')
        verbose_name_plural = _('restreamconfig_verbose_name_plural')

    def class_name(self):
        return _('restreamconfig_class_name')

    def get_absolute_url(self):
        return reverse('restream:restreamconfig_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} to {}'.format(self.stream, self.name)

    def get_json_config(self):
        config = {
            'name': self.name,
            'app': self.stream.application.name,
            'stream': str(self.stream.stream),
            'target': self.target,
            'format': self.format
        }
        return json.dumps(config)


pre_delete.connect(handlers.remove_obj_perms_connected_with_user, sender=RestreamConfig)
