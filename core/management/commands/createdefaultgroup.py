from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.conf import settings

PERMISSIONS = [
    'add_stream',
    'add_restreamconfig'
]


class Command(BaseCommand):
    help = 'Creates default user group with default permissions available to all users'

    def handle(self, *args, **options):
        default_group, _ = Group.objects.get_or_create(name=settings.DEFAULT_GROUP)
        for permission in PERMISSIONS:
            try:
                perm = Permission.objects.get(codename=permission)
            except Permission.DoesNotExist:
                print("permission '%s' does not exist" % permission)
                continue

            default_group.permissions.add(perm)
