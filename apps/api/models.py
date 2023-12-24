from django.db import models
from apps.user.models import User
from apps.main.models import Product, Table
from django.utils import timezone


# Create your models here.
class Order(models.Model):
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Mesa"
    )

    STATUS_CHOICES = [
        ("P", "Pendiente"),
        ("E", "Entregado"),
    ]
    order_status = models.CharField(
        choices=STATUS_CHOICES,
        default="P",
        max_length=1,
        verbose_name="Estado de la orden",
    )
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Empleado"
    )
    date = models.DateTimeField(default=timezone.now, verbose_name="Fecha")

    def __str__(self):
        return f"Orden de {self.table}"

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Ordenes"


class OrderDetails(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Orden"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Producto",
    )
    quantity = models.IntegerField(
        default=1, null=False, blank=False, verbose_name="Cantidad"
    )
    total = models.DecimalField(
        default=0.00, max_digits=9, decimal_places=2, verbose_name="Total"
    )

    def __str__(self):
        return f"Detalle de {self.order}"

    class Meta:
        verbose_name = "Detalle de orden"
        verbose_name_plural = "Detalles de orden"
