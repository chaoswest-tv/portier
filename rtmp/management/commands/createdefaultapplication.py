from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.conf import settings
from guardian.shortcuts import assign_perm

from rtmp import models


class Command(BaseCommand):
    help = 'Creates a default RTMP application that is available to all users in the default group'

    def handle(self, *args, **options):
        default_group, _ = Group.objects.get_or_create(name=settings.DEFAULT_GROUP)
        default_app, _ = models.Application.objects.get_or_create(name=settings.DEFAULT_RTMP_APPPLICATION)

        assign_perm('view_application', default_group, default_app)
