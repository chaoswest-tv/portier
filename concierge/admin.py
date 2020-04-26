from django.contrib import admin
from .models import Identity, Task, Claim


class IdentityAdmin(admin.ModelAdmin):
    fields = ['identity', 'name', 'notes', 'heartbeat']


class TaskAdmin(admin.ModelAdmin):
    fields = ['stream', 'type', 'configuration']


class ClaimAdmin(admin.ModelAdmin):
    fields = ['owner', 'task']


admin.site.register(Identity, IdentityAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Claim, ClaimAdmin)
