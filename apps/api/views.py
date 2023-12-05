from django.shortcuts import render
from .models import Order
from .serializers import OrderSerializer
from rest_framework.generics import ListCreateAPIView


# Create your views here.
class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
