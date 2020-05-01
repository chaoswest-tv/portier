from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from guardian.decorators import permission_required_or_403
from guardian.shortcuts import assign_perm

from . import models
from . import forms


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required_or_403('restream.add_restreamconfig'),
                  name='dispatch')
class RestreamConfigList(ListView):
    model = models.RestreamConfig


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required_or_403('restream.view_restreamconfig',
                  (models.RestreamConfig, 'pk', 'pk')),
                  name='dispatch')
class RestreamConfigDetail(DetailView):
    model = models.RestreamConfig


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required_or_403('restream.change_restreamconfig',
                  (models.RestreamConfig, 'pk', 'pk')),
                  name='dispatch')
class RestreamConfigChange(UpdateView):
    model = models.RestreamConfig
    form_class = forms.RestreamConfigFilteredStreamForm
    template_name_suffix = '_update_form'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required_or_403('restream.add_restreamconfig'),
                  name='dispatch')
class RestreamConfigCreate(CreateView):
    model = models.RestreamConfig
    form_class = forms.RestreamConfigFilteredStreamForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        valid = super().form_valid(form)
        if valid:
            user = self.request.user
            assign_perm('view_restreamconfig', user, self.object)
            assign_perm('change_restreamconfig', user, self.object)
            assign_perm('delete_restreamconfig', user, self.object)
        return valid


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required_or_403('restream.delete_restreamconfig',
                  (models.RestreamConfig, 'pk', 'pk')),
                  name='dispatch')
class RestreamConfigDelete(DeleteView):
    model = models.RestreamConfig
    success_url = reverse_lazy('restream:restreamconfig_list')
