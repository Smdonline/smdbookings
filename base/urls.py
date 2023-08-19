from django.urls import path, include
from . import views
from django.views.generic import ListView, DetailView
import core
app_name = 'base'

urlpatterns = [
    path('', views.index, name="main"),
    path('list/', ListView.as_view(template_name='location/list.html', model=core.models.Location), name='list'),
    path('<slug:slug>/', DetailView.as_view(template_name='location/detail.html', model=core.models.Location), name='detail'),

]
