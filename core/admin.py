from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

import core.models
# Register your models here.
from .models import User
from . import utils
from django.contrib.sites.models import Site
from . import forms


@admin.action(description="send user activation link")
def sent_user_activation_link(modeladmin, request, queryset):
    for obj in queryset:
        user = get_object_or_404(get_user_model(), pk=obj.pk)
        if not user.is_active:
            utils.send__activation_mail(user)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'is_staff')
    actions = [sent_user_activation_link]
    form = forms.UserCreationForm


@admin.register(core.models.Address)
class AddressAdmin(admin.ModelAdmin):
    form = forms.AddressForm
admin.site.unregister(Group)
