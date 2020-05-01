from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from .models import RestreamConfig


class RestreamConfigAdmin(GuardedModelAdmin):
    fields = ['name', 'active', 'stream', 'target']


admin.site.register(RestreamConfig, RestreamConfigAdmin)
