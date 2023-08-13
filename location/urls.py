from django.urls import path
from django.views.generic import ListView, CreateView, DetailView
from core import models
app_name = 'location'
urlpatterns = [
    path('', ListView.as_view(template_name='location/list.html', model=models.Location)),
]