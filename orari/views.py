from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse, get_object_or_404, Http404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from core.forms import OrariForm
import core.models


class CreateOrarioView(LoginRequiredMixin, CreateView):
    template_name = 'orari/add.html'
    success_url = reverse_lazy('users:profile')
    model = core.models.Orari
    form_class = core.forms.OrariForm

    def get_initial(self):
        location = get_object_or_404(core.models.Location, slug=self.kwargs.get('slug'))

        weekday = 0
        if 'weekday' in self.kwargs.keys():
            day = self.kwargs.get('weekday')
            if day in range(7):
                weekday = day
        return {'location': location, 'weekday': weekday, 'stars': '09:00'}


class UpdateOrari(LoginRequiredMixin, UpdateView):
    template_name = 'orari/add.html'
    success_url = reverse_lazy('users:profile')
    model = core.models.Orari
    fields = ('start', 'fine')

    def dispatch(self, request, *args, **kwargs):
        orar = get_object_or_404(core.models.Orari, id=kwargs.get('pk'))
        if orar.location.user == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        raise Http404
