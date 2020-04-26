from django.dispatch import Signal

stream_active = Signal(providing_args=['stream', 'params'])
stream_inactive = Signal(providing_args=['stream', 'params'])
