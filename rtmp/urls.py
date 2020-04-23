from django.urls import path
from . import views

urlpatterns = [
    path('callback/srs', views.callback_srs, name='callback_srs'),
]
