from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth
from apps.user.models import User
from apps.api.models import Order
from apps.main.models import Client


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

    total_orders = Order.objects.count()
    users_count = User.objects.count()
    clients_count = Client.objects.count()

    context = {
        "clients_count": clients_count,
        "users_count": users_count,
        "total_orders": total_orders,
        "orders_chart_data": {
            "months": months,
            "totals": totals,
        },
    }

    # No renderizamos la plantilla aquí, solo devolvemos el contexto
    return context


def index_view(request):
    return render(request, "accounts/sign-in.html")