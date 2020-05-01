import uuid

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.db.models.signals import pre_delete
from portier.common import handlers

from . import signals


class Application(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text=_("rtmp_application_name"))

    class Meta:
        verbose_name = _('application_verbose_name')
        verbose_name_plural = _('application_verbose_name_plural')

    def class_name(self):
        return _('aplication_class_name')

    def __str__(self):
        return self.name


class Stream(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, help_text=_('stream_application_help'))
    stream = models.UUIDField(unique=True, default=uuid.uuid4, help_text=_('stream_stream_help'))
    name = models.CharField(max_length=100, help_text=_('stream_name_help'))

    # the same stream uuid can be published multiple times to different origin
    # servers. this is a valid scheme to achieve a failover on the origin layer.
    # thus we need to keep track if a stream is published at least once,
    # and only send signals when we are going to / coming from 0 published streams.
    publish_counter = models.PositiveIntegerField(default=0)

    def on_publish(self, param):
        # if so far there were less than one incoming streams, this stream
        # is now being considered active
        if self.publish_counter < 1:
            signals.stream_active.send(sender=self.__class__,
                                       stream=str(self.stream),
                                       param=param
                                       )

        # keep track of this incoming stream
        self.publish_counter += 1
        self.save()

    def on_unpublish(self, param):
        # note that we now have on less incoming stream
        if self.publish_counter > 0:
            self.publish_counter -= 1

        # if we now have less than one incoming stream, this stream is being
        # considered inactive
        if self.publish_counter < 1:
            signals.stream_inactive.send(sender=self.__class__,
                                         stream=str(self.stream),
                                         param=param
                                         )
        self.save()

    def get_absolute_url(self):
        return reverse('rtmp:stream_detail', kwargs={'pk': self.pk})

    def class_name(self):
        return _('stream_class_name')

    def __str__(self):
        return self.name


pre_delete.connect(handlers.remove_obj_perms_connected_with_user, sender=Application)
pre_delete.connect(handlers.remove_obj_perms_connected_with_user, sender=Stream)
