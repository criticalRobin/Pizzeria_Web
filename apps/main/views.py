from django.shortcuts import render
from .models import Product, Table
from .serializers import ProductSerializer, TableSerializer
from rest_framework.generics import ListAPIView


# Create your views here.
class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class TableList(ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
