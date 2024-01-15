from django.urls import path
from .views import (
    payments_stats_view,
    employees_stats_view,
    clients_stats_view,
    orders_stats_view,
)

app_name = "home"

urlpatterns = [
    path("payments/", payments_stats_view, name="payments"),
    path("employees/", employees_stats_view, name="employees"),
    path("clients/", clients_stats_view, name="clients"),
    path("orders/", orders_stats_view, name="orders"),
]
