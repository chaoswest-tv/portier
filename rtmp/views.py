import json
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from . import models

logger = logging.getLogger(__name__)


@csrf_exempt
def callback_srs(request):
    if request.method != 'POST':
        return HttpResponse('1', status=405)

    try:
        json_data = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return HttpResponse('1', status=400)

    try:
        app_name = json_data['app']
        stream_name = json_data['stream']
        param = json_data['param']
    except KeyError:
        return HttpResponse('1', status=401)
    try:
        application = models.Application.objects.get(name=app_name)
        stream = models.Stream.objects.get(stream=stream_name, application=application)

    except ObjectDoesNotExist:
        return HttpResponse('1', status=401)

    if json_data.get('action') == 'on_publish':
        stream.on_publish(param=param)

    if json_data.get('action') == 'on_unpublish':
        stream.on_unpublish(param=param)

    return HttpResponse('0')
