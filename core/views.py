from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .tokens import account_activation_token
from django.utils.encoding import force_str as force_text
from django.contrib.auth import get_user_model

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import logout


def activate(request, uidb64, token):
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
