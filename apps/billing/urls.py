from django.urls import path
from .views import bill_pdf


app_name = "billing"

urlpatterns = [
    path("pdf/<int:pk>/", bill_pdf, name="bill_pdf"),
]
