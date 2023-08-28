from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse, get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView, UpdateView, DeleteView

import core.models


class CreateOrarioView(LoginRequiredMixin, CreateView):
    template_name = 'orari/add.html'
    success_url = reverse_lazy('users:profile')
    model = core.models.Orari
    form_class = core.forms.OrariForm


