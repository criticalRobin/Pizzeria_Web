# Generated by Django 4.2.7 on 2023-12-24 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Orden', 'verbose_name_plural': 'Ordenes'},
        ),
        migrations.AlterModelOptions(
            name='orderdetails',
            options={'verbose_name': 'Detalle de orden', 'verbose_name_plural': 'Detalles de orden'},
        ),
    ]
