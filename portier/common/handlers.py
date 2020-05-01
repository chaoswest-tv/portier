from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from guardian.models import UserObjectPermission
from guardian.models import GroupObjectPermission
from django.contrib.auth.models import User, Group
from django.conf import settings


def add_to_default_group(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        group = Group.objects.get(name=settings.DEFAULT_GROUP)
        user.groups.add(group)


def remove_obj_perms_connected_with_user(sender, instance, **kwargs):
    filters = Q(content_type=ContentType.objects.get_for_model(instance), object_pk=instance.pk)
    UserObjectPermission.objects.filter(filters).delete()
    GroupObjectPermission.objects.filter(filters).delete()
