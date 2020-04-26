import json

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now

from .models import Identity, Task


@csrf_exempt
@require_POST
def heartbeat(request, identity):
    try:
        id = Identity.objects.get(identity=identity)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'identity unknown'}, status=403)

    # update heartbeat
    id.heartbeat = now()
    id.save()

    # get current claims and available tasks
    claims = Task.objects.filter(claimed_by=id).all()
    available = Task.objects.filter(claimed_by=None).all()

    data = {
        'success': True,
        'claims': [{'uuid': str(o.uuid)} for o in list(claims)],
        'available': [{'uuid': str(o.uuid), 'type': o.type} for o in list(available)],
    }

    return JsonResponse(data)


@csrf_exempt
@require_POST
def claim(request, identity, task_uuid):
    try:
        id = Identity.objects.get(identity=identity)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'identity unknown'}, status=403)

    with transaction.atomic():
        try:
            task = Task.objects.get(uuid=task_uuid)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'task unknown'}, status=404)

        if task.claimed_by:
            return JsonResponse({'error': 'task already claimed'}, status=423)

        task.claimed_by = id
        task.save()

        data = {
            'success': True,
            'uuid': task.uuid,
            'type': task.type,
            'configuration': json.loads(task.configuration)
        }

        return JsonResponse(data)


@csrf_exempt
@require_POST
def release(request, identity, task_uuid):
    try:
        id = Identity.objects.get(identity=identity)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'identity unknown'}, status=403)

    with transaction.atomic():
        try:
            task = Task.objects.get(uuid=task_uuid)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'task unknown'}, status=404)

        if task.claimed_by != id:
            return JsonResponse({'error': 'task claimed by other identity'}, status=403)

        task.claimed_by = None
        task.save()

        data = {
            'success': True,
            'uuid': task.uuid,
            'type': task.type,
        }

        return JsonResponse(data)
