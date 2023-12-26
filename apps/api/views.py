from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Order, OrderDetails
from .serializers import OrderSerializer, OrderDetailsSerializer
from rest_framework.generics import ListCreateAPIView
from django.views.generic import ListView, UpdateView
from .forms import UpdateOrderDetailsForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class OrderListView(LoginRequiredMixin, ListView):
    login_url = "auth:login"
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


class OrderDetailUpdateView(UpdateView):
    model = OrderDetails
    template_name = "orders/update.html"
    form_class = UpdateOrderDetailsForm
    success_url = reverse_lazy("api:orders_list")

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())

        if form.is_valid():
            form.save()
            # Obtener todos los dispositivos registrados y enviar el mensaje
            devices = FCMDevice.objects.filter(active=True)
            devices.send_message(
                message=Message(
                    notification=Notification(
                        title="Plato listo", body=f"prueba de notificacion"
                    ),
                ),
                # this is optional
                # app=settings.FCM_DJANGO_SETTINGS['DEFAULT_FIREBASE_APP']
            )
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context["form"] = form
        return render(request, self.template_name, context)
