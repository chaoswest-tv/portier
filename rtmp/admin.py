from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from .models import Application, Stream


class ApplicationAdmin(GuardedModelAdmin):
    fields = ['name']


class StreamAdmin(GuardedModelAdmin):
    fields = ['application', 'stream', 'name', 'publish_counter']


admin.site.register(Application, ApplicationAdmin)
admin.site.register(Stream, StreamAdmin)
