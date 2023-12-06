from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from apps.main.models import Table


@receiver(post_save, sender=Order)
def updateAvailability(sender, instance, **kwargs):
    if instance.table:
        instance.table.available = False
        instance.table.save()
