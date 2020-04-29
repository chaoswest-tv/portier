from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from . import models


@method_decorator(login_required, name='dispatch')
class RestreamConfigList(ListView):
    model = models.RestreamConfig


@method_decorator(login_required, name='dispatch')
class RestreamConfigDetail(DetailView):
    model = models.RestreamConfig


@method_decorator(login_required, name='dispatch')
class RestreamConfigCreate(CreateView):
    model = models.RestreamConfig
    fields = ["name", "stream", "target", "active"]


@method_decorator(login_required, name='dispatch')
class RestreamConfigDelete(DeleteView):
    model = models.RestreamConfig
    success_url = reverse_lazy('restream:restreamconfig_list')
