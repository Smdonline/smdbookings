from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import core.models


# Create your views here.
class AddLocationView(CreateView):
    template_name = 'location/add_location.html'
    model = core.models.Location
    fields = '__all__'
    success_url = reverse_lazy('list')
