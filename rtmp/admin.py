from django.contrib import admin
from .models import Application, Stream


class ApplicationAdmin(admin.ModelAdmin):
    fields = ['name']


class StreamAdmin(admin.ModelAdmin):
    fields = ['application', 'stream', 'name']


admin.site.register(Application, ApplicationAdmin)
admin.site.register(Stream, StreamAdmin)
