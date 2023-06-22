from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path(
        'regConfirmed',
        views.Profile.as_view(template_name='users/registration/reg_confirmed.html'),
        name='regConfirmed'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path(_('register/'), views.UserRegistration.as_view(), name="register"),
]
