from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseCreationForm
from .models import User
from .utils import send__activation_mail



class UserCreationForm(BaseCreationForm):

    class Meta:
        model = User
        fields = (
             'name', 'email',
            'password1', 'password2',
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        send__activation_mail(user)
        return user
