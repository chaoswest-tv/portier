from django.urls import path
from . import views

urlpatterns = [
    path('api/<uuid:identity>/heartbeat', views.heartbeat, name='heartbeat'),
    path('api/<uuid:identity>/claim/<uuid:task_uuid>', views.claim, name='claim'),
    path('api/<uuid:identity>/release/<uuid:task_uuid>', views.release, name='release'),
]
