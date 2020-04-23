from django.contrib import admin
from .models import RestreamConfig


class RestreamConfigAdmin(admin.ModelAdmin):
    fields = ['name', 'active', 'stream', 'target']


admin.site.register(RestreamConfig, RestreamConfigAdmin)
