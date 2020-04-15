from django.dispatch import Signal

on_publish = Signal(providing_args=['application','streamkey','node'])
on_unpublish = Signal(providing_args=['application','streamkey','node'])
