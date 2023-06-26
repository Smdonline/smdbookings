# Generated by Django 4.2.2 on 2023-06-26 17:27

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_user_groups_user_is_superuser_user_user_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(blank=True, default='it', max_length=2)),
                ('region', models.CharField(max_length=255, verbose_name='regione')),
                ('province', models.CharField(max_length=255, verbose_name='provincie')),
                ('city', models.CharField(max_length=255, verbose_name='cita')),
                ('zip_code', models.CharField(max_length=5, verbose_name='CAP')),
                ('street_name', models.CharField(max_length=255, verbose_name='via')),
                ('street_number', models.PositiveSmallIntegerField(verbose_name='numero civico')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]
