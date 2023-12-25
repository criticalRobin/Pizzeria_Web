from django.urls import path
from .views import temp

app_name = "payment"

urlpatterns = [
    path("", temp, name="temp"),
]
