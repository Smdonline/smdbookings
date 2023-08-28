from django import forms
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseCreationForm
from django.core.validators import ValidationError
from localflavor.it import forms as it_forms

import core.models
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
        if not user.is_active:
            send__activation_mail(user)
        return user


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ('name',)


class LocationForm(forms.ModelForm):
    zip_code = it_forms.ITZipCodeField()

    class Meta:
        model = core.models.Location
        exclude = ('created', 'updated', 'user', 'slug')
        widgets = {
            'region': it_forms.ITRegionSelect,
            'province': it_forms.ITProvinceSelect,
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if core.models.Location.objects.filter(user=self.request.user).count() >= self.request.user.locations:
            raise ValidationError('%s has already a location' % self.request.user)
        return cleaned_data


class OrariForm(forms.ModelForm):
    class Meta:
        model = core.models.Orari
        fields = ('weekday', 'start', 'fine')

    def __init__(self, **kwargs):
        initial = kwargs.get("initial", {})

        super().__init__(**kwargs)