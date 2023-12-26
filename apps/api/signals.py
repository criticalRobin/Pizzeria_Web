from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderDetails
from apps.main.models import Table


@receiver(post_save, sender=Order)
def updateAvailability(sender, instance, **kwargs):
    if instance.table:
        instance.table.available = False
        instance.table.save()


@receiver(post_save, sender=OrderDetails)
def update_order_status(sender, instance, **kwargs):
    order = instance.order
    total_details = order.orderdetails_set.count()
    delivered_details = order.orderdetails_set.filter(detail_status="E").count()

    if total_details == delivered_details:
        order.order_status = "E"
    elif delivered_details > 0:
        order.order_status = "P"
    order.save()