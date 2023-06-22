"""
URL configuration for the  project.


"""
from django.contrib import admin
from django.urls import path, include

from users import urls as user_urls
from base import urls as base_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(user_urls)),
    path('', include(base_urls)),
]
