from django.db import models
from apps.main.models import Client
from apps.api.models import Order
from django.utils import timezone


# Create your models here.
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Orden")
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name="Cliente", null=True, blank=True
    )
    PAYMENT_CHOICES = (
        ("E", "Efectivo"),
        ("T", "Tarjeta"),
    )
    payment_method = models.CharField(
        max_length=1, choices=PAYMENT_CHOICES, verbose_name="Método de pago"
    )
    stripe_transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="ID de Transacción de Stripe",
    )
    amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Monto")
    STATUS_CHOICES = (
        ("P", "Pendiente"),
        ("C", "Pagado"),
    )
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name="Estado"
    )
    payment_date = models.DateTimeField(
        default=timezone.now, verbose_name="Fecha de Pago"
    )

    def __str__(self):
        return f"Pago {self.id} para {self.order}"

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
