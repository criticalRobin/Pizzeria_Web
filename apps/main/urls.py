from django.urls import path
from .views import ProductList, TableList


app_name = "main"

urlpatterns = [
    path("list/products", ProductList.as_view(), name="products_list"),
    path("list/tables", TableList.as_view(), name="tables_list"),
]
