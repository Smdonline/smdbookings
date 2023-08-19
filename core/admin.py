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
    list_display = ('email', 'name', 'locations', 'is_active', 'is_staff')
    actions = [sent_user_activation_link]
    form = forms.UserCreationForm




@admin.register(core.models.Orari)
class OrariAdmin(admin.ModelAdmin):
    list_display = ('weekday','start','fine','durata_apertura')
    sortable_by = ('weekday','start')
    ordering = ('start','weekday')
    list_filter = ('weekday',)

@admin.register(core.models.Location)
class AdminLocation(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',)
    }
    readonly_fields = ('user','name','slug')

admin.site.unregister(Group)