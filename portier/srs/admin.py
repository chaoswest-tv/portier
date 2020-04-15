from django.contrib import admin
from .models import Application, Streamkey


class ApplicationAdmin(admin.ModelAdmin):
    fields = ['name']


class StreamkeyAdmin(admin.ModelAdmin):
    fields = ['application', 'key', 'name']


admin.site.register(Application, ApplicationAdmin)
admin.site.register(Streamkey, StreamkeyAdmin)
