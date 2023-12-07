from django.shortcuts import render
from .models import Order
from .serializers import OrderSerializer, OrderDetailsSerializer
from rest_framework.generics import ListCreateAPIView
from django.views.generic import ListView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# Create your views here.


class OrderListView(ListView):
    model = Order
    template_name = "orders/list.html"

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context["orders"] = Order.objects.prefetch_related("orderdetails_set").all()
        return context


class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        channel_layer = get_channel_layer()

        # Serializar la información de la orden, incluyendo los detalles
        order_details = OrderDetailsSerializer(
            order.orderdetails_set.all(), many=True
        ).data

        order_data = {
            "text": "Nueva orden creada",
            "table": order.table.number
            if hasattr(order.table, "number")
            else str(order.table),
            "details": order_details,  # Esto incluirá los detalles de la orden
        }

        async_to_sync(channel_layer.group_send)(
            "orders", {"type": "order.update", "message": order_data}
        )
