from django.contrib import admin
from .models import Identity, Task


class IdentityAdmin(admin.ModelAdmin):
    fields = ['identity', 'name', 'notes', 'heartbeat']


class TaskAdmin(admin.ModelAdmin):
    fields = ['stream', 'type', 'config_id', 'configuration', 'claimed_by']


admin.site.register(Identity, IdentityAdmin)
admin.site.register(Task, TaskAdmin)
