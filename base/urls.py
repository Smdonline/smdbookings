from django.urls import path, include
from . import views


app_name = 'base'

urlpatterns = [
    path('', views.index, name="main"),
    path('location/', include('location.urls'), name='location')
]
