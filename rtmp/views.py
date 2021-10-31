import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.admin.utils import NestedObjects
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from guardian.decorators import permission_required_or_403
from guardian.shortcuts import assign_perm

from . import models
from . import forms

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
        # QUIRK this is a weird bug when pushing from OME to SRS. wtf.
        # for some reason srs interprets the incoming app as app/stream, and passes this on to portier.
        # only keep the stuff infront of a (potential) slash, and throw away the rest. problem solved^tm
        app_name = app_name.split('/')[0]
        # ENDQUIRK
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


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required_or_403('rtmp.add_stream'),
                  name='dispatch')
class StreamList(ListView):
    model = models.Stream


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required_or_403('rtmp.view_stream',
                  (models.Stream, 'pk', 'pk')),
                  name='dispatch')
class StreamDetail(DetailView):
    model = models.Stream


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required_or_403('rtmp.change_stream',
                  (models.Stream, 'pk', 'pk')),
                  name='dispatch')
class StreamChange(UpdateView):
    model = models.Stream
    form_class = forms.StreamFilteredApplicationForm
    template_name_suffix = '_update_form'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required_or_403('rtmp.add_stream'),
                  name='dispatch')
class StreamCreate(CreateView):
    model = models.Stream
    form_class = forms.StreamFilteredApplicationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        valid = super().form_valid(form)
        if valid:
            user = self.request.user
            assign_perm('view_stream', user, self.object)
            assign_perm('change_stream', user, self.object)
            assign_perm('delete_stream', user, self.object)
        return valid


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required_or_403('rtmp.delete_stream',
                  (models.Stream, 'pk', 'pk')),
                  name='dispatch')
class StreamDelete(DeleteView):
    model = models.Stream
    success_url = reverse_lazy('rtmp:stream_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        collector = NestedObjects(using='default')
        collector.collect([self.object])

        context['to_delete'] = collector.nested()

        print(context['to_delete'])
        return context
