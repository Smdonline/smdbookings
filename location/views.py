from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView

import core.models


# Create your views here.
class AddLocationView(CreateView):
    template_name = 'location/add.html'
    model = core.models.Location
    fields = '__all__'