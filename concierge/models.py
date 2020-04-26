import uuid
from django.db import models
from rtmp.models import Stream


class Identity(models.Model):
    # models a concierge identity. every running concierge needs to have a
    # unique identity that is being used for task claims, etc.
    identity = models.CharField(max_length=36, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    notes = models.TextField()

    # heartbeat indicates last point in time that this identity was seen.
    # some cronjob should scan the heartbeats and release all claims by
    # identities that have not been seen in a while. this interval should
    # be quite short so that the tasks can be claimed by other identities asap.
    heartbeat = models.DateTimeField(blank=True)


class Task(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    configuration = models.TextField()


class Claim(models.Model):
    owner = models.ForeignKey(Identity, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
