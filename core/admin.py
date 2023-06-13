from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email','name')

admin.site.unregister(Group)