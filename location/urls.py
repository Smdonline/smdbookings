from django.urls import path
from django.views.generic import ListView, CreateView, DetailView
from core import models
from . import views

app_name = 'location'
urlpatterns = [

    path('add/', views.AddLocationView.as_view(), name='add'),
    # path('edit/<slug:loc_slug>/', views.edit_location, name='edit'),
    # path('delete/<slug:loc_slug>/', views.delete_location, name='delete'),
]