"""Models for the smdbookings project"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import (
    AbstractBaseUser,
    BaseUserManager
)
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

days = [
    (0, _("Monday")), (1, _("Tuesday")), (2, _("Wednesday")),
    (3, _("Thursday")), (4, _("Friday")), (5, _("Saturday")),
    (6, _("Sunday"))
]


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
    locations = models.PositiveSmallIntegerField(default=1)

    objects = UserManager()

    USERNAME_FIELD = 'email'


"""Location models"""



def profile_upload_path(instance,filename):
    ext = filename.split(".")[-1]
    filename="%s.%s" % (instance.slug, ext)
    import os
    return os.path.join("media/locations/%s/%s" % (instance.user, instance.slug), filename)
class Location(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_location')
    name = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(_('location image'), upload_to=profile_upload_path, blank=True)

    description = models.TextField(_('description'), default=None)

    country = CountryField(blank=True, default='it')
    region = models.CharField(_('regione'), blank=False, max_length=255)
    province = models.CharField(_('provincie'), blank=False, max_length=255)
    city = models.CharField(_('cita'), max_length=255, blank=False)
    zip_code = models.CharField(_('CAP'), max_length=5, )
    street_name = models.CharField(_('via'), max_length=255, blank=False)
    street_number = models.PositiveSmallIntegerField(_('numero civico'))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug
    def get_orari(self):
        querry = Orari.objects.filter(location=self)

        orari = {}
        for numar, zi in days:
            orari[zi] = [i for i in querry if i.weekday == numar]
        return orari

    def orariile_mele(self):
        return self.location_schedule.order_by('weekday', 'start')
class Orari(models.Model):
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE,
        related_name='location_schedule',
        default=None)

    weekday = models.PositiveSmallIntegerField(
        _('nome giorno settimana'), choices=days
    )
    start = models.TimeField(_('ora inizio'))
    fine = models.TimeField(_('ora fine'))
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['weekday', 'start', 'location'],
                name='unique_day_start',
            )
        ]
        index_together = ('weekday', 'start')
        verbose_name = _("orario apertura")
        verbose_name_plural = _("orari apertura")

    def get_day_name(self):
        return days[self.weekday][1]

    def get_start_to_timedelta(self):
        return timedelta(hours=self.start.hour, minutes=self.start.minute)

    def get_fine_to_timedelta(self):
        fine = timedelta(hours=self.fine.hour, minutes=self.fine.minute)
        if fine <= self.get_start_to_timedelta():
            fine = fine + timedelta(days=1)
        return fine

    def get_day_openings(self, day):
        if day in days:
            return Orari.objects.all().filter(weekday=self.weekday, location=self.location).order_by('start')

    def durata_apertura(self):
        start = self.get_start_to_timedelta()
        fine = self.get_fine_to_timedelta()
        return fine - start

    def __str__(self):
        return '(%s -- %s)' % (self.start, self.fine)
