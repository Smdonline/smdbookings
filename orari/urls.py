from django.urls import path, include
from . import views
app_name = 'orari'
urlpatterns = [
    path('<slug:slug>/', views.CreateOrarioView.as_view(), name="add_orario"),
]