"""Models for the smdbookings project"""

from django.db import models
from django.contrib.auth.base_user import (
    AbstractBaseUser,
    BaseUserManager
)
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from localflavor.it import forms, util


class UserManager(BaseUserManager):
    """Manager for the  custom user model"""

    def create_user(self, email, password=None, **extra_fields):
        """Create user with given email and password"""
        if not email:
            raise ValueError(_('User must have an email'))
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    def create_superuser(self, email, password):
        """Create a superuser with email and password"""
        user = self.create_user(email=email, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User system for the project email as username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


"""Location models"""


class Address(models.Model):
    country = CountryField(blank=True, default='it')
    region = models.CharField(_('regione'), blank=False, max_length=255)
    province = models.CharField(_('provincie'), blank=False, max_length=255)
    city = models.CharField(_('cita'), max_length=255, blank=False)
    zip_code = models.CharField(_('CAP'), max_length=5, )
    street_name = models.CharField(_('via'), max_length=255, blank=False)
    street_number = models.PositiveSmallIntegerField(_('numero civico'))


class Location(models.Model):
    name = models.CharField(max_length=255, blank=False)
