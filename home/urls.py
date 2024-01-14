from django.urls import path
from .views import payments_stats_view

app_name = "home"

urlpatterns = [
    path("payments/", payments_stats_view, name="payments"),
]
