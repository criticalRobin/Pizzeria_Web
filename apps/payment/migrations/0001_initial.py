# Generated by Django 4.2.7 on 2024-01-09 04:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0006_order_total'),
        ('main', '0003_alter_client_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('E', 'Efectivo'), ('T', 'Tarjeta')], max_length=1, verbose_name='Método de pago')),
                ('stripe_transaction_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='ID de Transacción de Stripe')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Monto')),
                ('status', models.CharField(choices=[('P', 'Pendiente'), ('C', 'Pagado')], max_length=1, verbose_name='Estado')),
                ('payment_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de Pago')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.client', verbose_name='Cliente')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.order', verbose_name='Orden')),
            ],
            options={
                'verbose_name': 'Pago',
                'verbose_name_plural': 'Pagos',
            },
        ),
    ]
