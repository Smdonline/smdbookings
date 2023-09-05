from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse, get_object_or_404,render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.views.generic import CreateView, UpdateView, DeleteView
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
        return {'location': location, 'weekday': weekday}

# @login_required()
# def add_orario(request, slug):
#     location = get_object_or_404(core.models.Location, slug=slug, user=request.user)
#     if request.method == "POST":
#         form = OrariForm(request.POST)
#         if form.is_valid():
#             orario = form.save(commit=False)
#             orario.save()
#             return reverse_lazy('users:profile')
#     else:
#
#         form = OrariForm(initial={'location': location})
#         return render(request, 'orari/add.html', {'form': form})
#



