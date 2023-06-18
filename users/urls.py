from django.urls import path
from django.utils.translation import gettext_lazy as _
from core import views as core_views
from django.views.generic import TemplateView
from . import views
urlpatterns = [
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path('regConfirmed', TemplateView.as_view(template_name='core/reg_confirmed.html'), name='regConfirmed'),
    path(_('register/'), views.UserRegistration.as_view(),name="register"),
]