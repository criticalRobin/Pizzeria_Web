from django.urls import path
from .views import OrderListCreateView

app_name = "api"

urlpatterns = [
    path("orders/", OrderListCreateView.as_view(), name="orders"),
]
