from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from apps.api.models import Order
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
        context["orders"] = orders_to_pay
        print(context["orders"])
        return context


@login_required
def create_order_payment(request, order_id):
    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    order = Order.objects.get(id=order_id)

    # Crear line_items con price_data basado en los detalles de la orden para Stripe
    line_items = [
        {
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "Orden #" + str(order.id),
                },
                "unit_amount": int(order.total * 100),
            },
            "quantity": 1,
        }
    ]

    # Crear la sesión de pago de Stripe
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

    # Crear un registro de pago en la base de datos, si es necesario
    Payment.objects.create(
        order=order,
        # Asegúrese de ajustar la siguiente línea para que refleje cómo se obtiene el cliente en su sistema
        client=Client.objects.get(id=1),
        amount=order.total,
        stripe_transaction_id=checkout_session["id"],
        status="P",  # Pendiente
        payment_method="T",  # Tarjeta
        payment_date=timezone.now(),  # Importar timezone si aún no se ha hecho
    )

    # Redirigir al usuario a la sesión de pago de Stripe
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
    return render(request, "payment/", {"order": order})


def payment_cancelled(request, order_id):
    render(request, "payment/", {"order_id": order_id})
