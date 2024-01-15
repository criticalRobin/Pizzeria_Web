from django.urls import path
from .views import (
    OrdersToPayListView,
    create_order_payment,
    payment_success,
    payment_cancelled,
    PaymentCreateView,
)

app_name = "payment"

urlpatterns = [
    path("", OrdersToPayListView.as_view(), name="temp"),
    path(
        "order/payment/<int:order_id>/",
        create_order_payment,
        name="create_order_payment",
    ),
    path(
        "order/payment/success/<int:order_id>/",
        payment_success,
        name="payment_success",
    ),
    path(
        "order/payment/cancelled/<int:order_id>/",
        payment_cancelled,
        name="payment_cancelled",
    ),
    path("create/<int:pk>/", PaymentCreateView.as_view(), name="money_payment"),
]
