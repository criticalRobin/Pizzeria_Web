# Generated by Django 4.2.7 on 2024-01-11 20:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_client_address_alter_client_dni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator(code='invalid_phone', message='El número de teléfono debe contener solo números.', regex='^[0-9]+$')], verbose_name='Teléfono'),
        ),
    ]
