import json
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from . import models

logger = logging.getLogger(__name__)


@csrf_exempt
def callback(request):
    if request.method != 'POST':
        return HttpResponse('1', status=405)

    json_data = json.loads(request.body)

    try:
        client_ip = json_data['ip']
        client_id = json_data['client_id']
        vhost = json_data['vhost']
        param = json_data['param']
        app_name = json_data['app']
        stream_name = json_data['stream']
    except KeyError:
        return HttpResponse('1', status=401)
    try:
        application = models.Application.objects.get(name=app_name)
        streamkey = models.Streamkey.objects.get(key=stream_name, application=application)

    except ObjectDoesNotExist:
        return HttpResponse('1', status=401)

    if json_data.get('action') == 'on_publish':
        streamkey.on_publish(client_ip=client_ip,
                             client_id=client_id,
                             vhost=vhost,
                             param=param
                             )

    if json_data.get('action') == 'on_unpublish':
        streamkey.on_unpublish(client_ip=client_ip,
                               client_id=client_id,
                               vhost=vhost,
                               param=param
                               )

    return HttpResponse('0')
