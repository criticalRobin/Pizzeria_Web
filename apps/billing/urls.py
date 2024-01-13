from django.urls import path
from .views import bill_pdf, BillListView


app_name = "billing"

urlpatterns = [
    path("pdf/<int:pk>/", bill_pdf, name="bill_pdf"),
    path("list/", BillListView.as_view(), name="bill_list"),
]
