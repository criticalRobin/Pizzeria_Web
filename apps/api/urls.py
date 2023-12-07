from django.urls import path
from .views import OrderListCreateView, OrderListView

app_name = "api"

urlpatterns = [
    path("orders/", OrderListCreateView.as_view(), name="orders"),
    path("orders/list/", OrderListView.as_view(), name="orders_list"),
]
