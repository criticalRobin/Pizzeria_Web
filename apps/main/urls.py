from django.urls import path
from .views import ProductList


app_name = "main"

urlpatterns = [
    path("list/products", ProductList.as_view(), name="products_list"),
]
