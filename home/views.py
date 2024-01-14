from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncDay
from apps.user.models import User
from apps.api.models import Order, OrderDetails
from apps.main.models import Client
from apps.payment.models import Payment
from django.db.models import Count, Sum, F
import json


# Create your views here.
def dashboard_stats_view(request):
    orders_by_month = (
        Order.objects.annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    months = [order["month"].strftime("%b") for order in orders_by_month]
    totals = [order["total"] for order in orders_by_month]

    daily_revenue = (
        Payment.objects.annotate(day=TruncDay("payment_date"))
        .values("day")
        .annotate(total=Sum("amount"))
        .order_by("day")
    )
    daily_revenue_data = {
        "days": [revenue["day"].strftime("%Y-%m-%d") for revenue in daily_revenue],
        "totals": [float(revenue["total"]) for revenue in daily_revenue],
    }

    total_orders = Order.objects.count()
    users_count = User.objects.count()
    clients_count = Client.objects.count()
    total_money_payments = Payment.objects.aggregate(total=Sum("amount"))["total"]

    context = {
        "clients_count": clients_count,
        "users_count": users_count,
        "total_orders": total_orders,
        "total_money_payments": total_money_payments,
        "orders_chart_data": {
            "months": months,
            "totals": totals,
        },
        "daily_revenue_data": daily_revenue_data,
    }
    return context


def payments_stats_view(request):
    money_payments_by_month = (
        Payment.objects.annotate(month=TruncMonth("payment_date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )
    payment_months = [
        payment["month"].strftime("%b") for payment in money_payments_by_month
    ]
    money = [float(payment["total"]) for payment in money_payments_by_month]

    daily_revenue = (
        Payment.objects.annotate(day=TruncDay("payment_date"))
        .values("day")
        .annotate(total=Sum("amount"))
        .order_by("day")
    )
    daily_revenue_data = {
        "days": [revenue["day"].strftime("%Y-%m-%d") for revenue in daily_revenue],
        "totals": [float(revenue["total"]) for revenue in daily_revenue],
    }

    payment_methods_totals = (
        Payment.objects.values("payment_method")
        .annotate(total_amount=Sum("amount"))
        .order_by("payment_method")
    )
    payment_methods = [
        (
            payment.get("payment_method"),
            Payment.objects.filter(payment_method=payment.get("payment_method"))
            .first()
            .get_payment_method_display(),
        )
        for payment in payment_methods_totals
    ]
    amounts = [float(payment["total_amount"]) for payment in payment_methods_totals]

    product_revenue = (
        OrderDetails.objects.values("product__name")
        .annotate(revenue=Sum(F("quantity") * F("product__sale_price")))
        .order_by("-revenue")
    )
    product_names = [item["product__name"] for item in product_revenue]
    revenues = [float(item["revenue"]) for item in product_revenue]

    context = dashboard_stats_view(request)
    context["payments_chart_data"] = {
        "months_payments": payment_months,
        "money": money,
    }
    context["daily_revenue_data"] = daily_revenue_data
    context["payment_methods"] = payment_methods
    context["amounts"] = amounts
    context["product_names"] = product_names
    context["revenues"] = revenues

    return render(request, "admin/payment-stats.html", context)


def employees_stats_view(request):
    role_counts = (
        User.objects.values("employee_role")
        .annotate(total=Count("employee_role"))
        .order_by("employee_role")
    )
    roles = [role["employee_role"] for role in role_counts]
    counts = [role["total"] for role in role_counts]
    role_labels = {
        "admin": "Administrador",
        "waiter": "Mesero",
        "cashier": "Cajero",
        "chef": "Cocinero",
    }
    role_names = [role_labels[role] for role in roles]

    context = dashboard_stats_view(request)
    context["role_names"] = role_names
    context["counts"] = counts

    return render(request, "admin/employees-stats.html", context)


def index_view(request):
    return render(request, "accounts/sign-in.html")
