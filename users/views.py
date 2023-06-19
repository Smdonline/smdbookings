from django.views.generic import CreateView


from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from core.tokens import account_activation_token
from django.utils.encoding import force_str as force_text
from django.contrib.auth import get_user_model
from core.forms import UserCreationForm
from core.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import logout
from django.urls import reverse_lazy



def activate(request, uidb64, token):
    """view to activate user based on link sent"""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token) and not user.is_active:
        user.is_active = True
        user.save()
        return redirect('regConfirmed')
    else:
        return HttpResponse('Activation link is invalid!')


class UserRegistration(CreateView):
    template_name = 'users/registration/registration.html'
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('regConfirmed')
