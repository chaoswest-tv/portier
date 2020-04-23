from django.dispatch import Signal

on_publish = Signal(providing_args=['application', 'stream', 'params'])
on_unpublish = Signal(providing_args=['application', 'stream', 'params'])
