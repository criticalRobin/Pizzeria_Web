from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from apps.api.models import Order, OrderDetails
from apps.main.models import Client
from .models import Payment
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import stripe


# Create your views here.
class OrdersToPayListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "temp.html"

    def get_context_data(self, **kwargs):
        context = super(OrdersToPayListView, self).get_context_data(**kwargs)
        orders_to_pay = Order.objects.filter(order_status="E")
        orders_to_pay_details = OrderDetails.objects.filter(order__in=orders_to_pay)
        context["orders"] = orders_to_pay
        context["order_details"] = orders_to_pay_details
        return context


@login_required
def create_order_payment(request, order_id):
    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    order = Order.objects.get(id=order_id)
    details = OrderDetails.objects.filter(order=order)

    line_items = [
        {
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": detail.product.name,
                },
                "unit_amount": int(
                    detail.product.sale_price * 100
                ), 
            },
            "quantity": detail.quantity,
        }
        for detail in details
    ]

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("payment:payment_success", args=[order.id])
        )
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(
            reverse("payment:payment_cancelled", args=[order.id])
        ),
    )

    Payment.objects.create(
        order=order,
        client=Client.objects.get(id=1),
        amount=order.total,
        stripe_transaction_id=checkout_session["id"],
        status="P",
        payment_method="T",
        payment_date=timezone.now(),
    )

    return redirect(checkout_session.url, code=303)


def payment_success(request, order_id):
    order = Order.objects.get(id=order_id)
    payment = Payment.objects.get(order=order)

    # Actualizar el registro de pago
    payment.status = "C"  # Completado
    payment.save()

    # Actualizar el estado de la orden
    order.order_status = "C"  # Cancelado
    order.save()

    # Redirigir al usuario a la página de éxito
    return render(request, "success.html", {"order": order})


def payment_cancelled(request, order_id):
    render(request, "payment/", {"order_id": order_id})
