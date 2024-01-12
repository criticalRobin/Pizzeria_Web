# Generated by Django 4.2.7 on 2024-01-11 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_order_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('P', 'Pendiente'), ('E', 'Entregado'), ('C', 'Cancelado')], default='P', max_length=1, verbose_name='Estado de la orden'),
        ),
    ]