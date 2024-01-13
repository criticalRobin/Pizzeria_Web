from django.urls import path
from .views import OrderListCreateView, OrderListView, OrderDetailUpdateView, OrderListUpdateView

app_name = "api"

urlpatterns = [
    path("orders/", OrderListCreateView.as_view(), name="orders"),
    path("orders/<int:pk>/", OrderListUpdateView.as_view(), name="order_update"),
    path("orders/list/", OrderListView.as_view(), name="orders_list"),
    path(
        "orders/update/<int:pk>/",
        OrderDetailUpdateView.as_view(),
        name="orders_update",
    ),
]
