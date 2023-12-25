from django.urls import path
from .views import ProductList, TableList, update_device_token


app_name = "main"

urlpatterns = [
    path("list/products", ProductList.as_view(), name="products_list"),
    path("list/tables", TableList.as_view(), name="tables_list"),
    path("update/device", update_device_token, name="update_device_token"),
]
