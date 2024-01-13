from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order, OrderDetails
from apps.main.models import Table


@receiver(post_save, sender=Order)
def updateAvailability(sender, instance, **kwargs):
    if instance.table:
        instance.table.available = False
        instance.table.save()


@receiver(post_save, sender=OrderDetails)
def update_order_status(sender, instance, created, **kwargs):
    order = instance.order
    if order.order_status != 'C':
        total_details = order.orderdetails_set.count()
        delivered_details = order.orderdetails_set.filter(detail_status="E").count()
        ready_details = order.orderdetails_set.filter(detail_status="L").count()
        if total_details == delivered_details + ready_details:
            order.order_status = "E"
        elif created or delivered_details > 0:
            order.order_status = "P"
        order.save()

@receiver(post_save, sender=OrderDetails)
def delete_orderdetail_if_quantity_zero(sender, instance, **kwargs):
    if instance.quantity == 0:
        instance.delete()

@receiver(pre_save, sender=Order)
def update_order_status_on_delete(sender, instance, **kwargs):
    order = instance
    if order.order_status != 'C':
        total_details = order.orderdetails_set.count()
        delivered_details = order.orderdetails_set.filter(detail_status="E").count()
        ready_details = order.orderdetails_set.filter(detail_status="L").count()
        print(total_details, delivered_details, ready_details)
        if total_details == delivered_details + ready_details:  # Resta 1 a total_details
            order.order_status = "E"
            print(order.order_status, order.id)
  