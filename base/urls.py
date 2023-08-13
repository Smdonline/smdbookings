from django.urls import path, include
from . import views
from location import urls as location_urls

app_name = 'base'

urlpatterns = [
    path('', views.index, name="main"),
    path('location/',include('location_urls'))
]
