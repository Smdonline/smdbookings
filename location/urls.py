from django.urls import path
from django.views.generic import ListView, CreateView, DetailView
from core import models
from . import views

app_name = 'location'
urlpatterns = [
    path('', ListView.as_view(template_name='location/list.html', model=models.Location), name='list'),
    path('add/', views.AddLocationView.as_view(), name='add'),
    # path('edit/<slug:loc_slug>/', views.edit_location, name='edit'),
    # path('delete/<slug:loc_slug>/', views.delete_location, name='delete'),
]