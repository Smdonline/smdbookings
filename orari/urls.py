from django.urls import path, include
from . import views
app_name = 'orari'
urlpatterns = [
    path('update/<int:pk>/', views.UpdateOrari.as_view(), name='update'),
    path('<slug:slug>/', views.CreateOrarioView.as_view(), name="add_orario"),
    path('<slug:slug>/<int:weekday>/', views.CreateOrarioView.as_view(), name="add_orario"),

]
