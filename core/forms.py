from django import forms
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseCreationForm
from django.core.validators import ValidationError
from localflavor.it import forms as it_forms
from django.utils.translation import gettext_lazy as _
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
        fields = ('location', 'weekday', 'start', 'fine')
        widgets = {
            'weekday': forms.Select(attrs={'class': 'form-select'}),
            'user': forms.HiddenInput(),
            'start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-select'}),
            'fine': forms.TimeInput(attrs={'type': 'time', 'class': 'form-select'})
        }
    def  clean(self):
        clean_data = super().clean()

        orar = core.models.Orari(
            location=clean_data.get('location'),
            weekday=clean_data.get('weekday'),
            start=clean_data.get('start'),
            fine=clean_data.get('fine')
        )
        allByDay = core.models.Orari.objects.all().filter(weekday=orar.weekday, location=orar.location)
        if allByDay:
            for hour in allByDay:
                start = hour.get_start_to_timedelta()
                fine = hour.get_fine_to_timedelta()
                if start < orar.get_start_to_timedelta() < fine:
                    raise ValidationError(
                        _('esiste gia un orario %s con che contiene questa ora %s' % (hour, start))
                    )
                if start > orar.get_start_to_timedelta() > fine:
                    raise ValidationError(
                        _('esiste gia un orario %s con che contiene questo  orario provi a mofificarlo ' % hour)
                    )
                if start < orar.get_fine_to_timedelta() <= fine:
                    raise ValidationError(
                        _('esiste gia un orario %s con che contiene questo  orario provi a mofificarlo ' % hour)
                    )
                if orar.get_start_to_timedelta() <= start and orar.get_fine_to_timedelta() >= fine:
                    raise ValidationError(
                        _('esiste gia un orario %s con che contiene questo  orario provi a mofificarlo ' % hour)
                    )
        return clean_data
