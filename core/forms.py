from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

import core.models
from .models import User
from .utils import send__activation_mail
from localflavor.it import forms as it_forms


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
        if not user.is_active:
            send__activation_mail(user)
        return user


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ('name',)


class AddressForm(forms.ModelForm):
    zip_code = it_forms.ITZipCodeField()

    class Meta:
        model = core.models.Address
        fields = '__all__'
        widgets = {
            'region': it_forms.ITRegionSelect,
            'province': it_forms.ITProvinceSelect,
        }
