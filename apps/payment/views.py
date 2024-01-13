from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from apps.api.models import Order, OrderDetails
from apps.main.models import Client, Entity
from apps.billing.models import Bill
from .models import Payment
from .forms import CreatePaymentForm
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


class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = CreatePaymentForm
    template_name = "create.html"
    success_url = reverse_lazy("payment:temp")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get("pk")
        if order_id:
            order = get_object_or_404(Order, id=order_id)
            orders_to_pay_details = OrderDetails.objects.filter(order=order)
            clients = Client.objects.all()
            context["order"] = order
            context["order_details"] = orders_to_pay_details
            context["clients"] = clients
        return context

    def get(self, request, *args, **kwargs):
        self.request.session["current_order_id"] = kwargs["pk"]
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        order_id = kwargs["pk"]
        order = get_object_or_404(Order, id=order_id)
        form = self.form_class(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)
            client_id = request.POST.get("client_id")
            if client_id:
                payment.client = Client.objects.get(id=client_id)
            payment.order = order
            payment.payment_method = "E"
            payment.amount = order.total
            payment.status = "C"
            payment.payment_date = timezone.now()

            order.order_status = "C"
            order.save()

            table = order.table
            if not table.available:
                table.available = True
                table.save()

            payment.save()

            Bill.objects.create(entity=Entity.objects.get(id=1), payment=payment)
            return HttpResponseRedirect(self.success_url)

        context = self.get_context_data(**kwargs)
        context["form"] = form
        return render(request, self.template_name, context)


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
                "unit_amount": int(detail.product.sale_price * 100),
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
        client=None,
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
    table = order.table
    session_id = request.GET.get("session_id")
    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN

    Bill.objects.create(entity=Entity.objects.get(id=1), payment=payment)

    if session_id:
        session = stripe.checkout.Session.retrieve(session_id)
        customer_email = session.get("customer_details", {}).get("email", None)
        name = session.get("customer_details", {}).get("name", None)

        if name is not None:
            complete_name = name.split(" ")
            first_name = complete_name[0]
            last_name = complete_name[1]

    payment.status = "C"
    client_check = Client.objects.filter(email=customer_email).exists()

    if not client_check:
        payment.client = Client.objects.create(
            dni=None,
            name=first_name,
            surname=last_name,
            address=None,
            phone_number=None,
            email=customer_email,
        )
    else:
        payment.client = Client.objects.get(email=customer_email)
    payment.save()

    order.order_status = "C"
    order.save()

    if table.available is False:
        table.available = True
        table.save()

    return render(request, "success.html", {"order": order})


def payment_cancelled(request, order_id):
    render(request, "payment/", {"order_id": order_id})
