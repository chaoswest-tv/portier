from django.db import models
from django.utils.translation import gettext as _
import uuid

from . import signals


class Application(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text=_("rtmp_application_name"))

    def __str__(self):
        return self.name


class Stream(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    stream = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)

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
                                       stream=self.stream,
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
                                         stream=self.stream,
                                         param=param
                                         )
        self.save()

    def __str__(self):
        return self.name
