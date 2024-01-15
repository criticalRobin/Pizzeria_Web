from django.db import models
from apps.main.models import Entity
from apps.payment.models import Payment


# Create your models here.
class Bill(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, verbose_name="Entidad")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, verbose_name="Pago")

    def __str__(self):
        return f"Factura {self.id} para {self.payment}"

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
