from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .models import Product, Table, Client
from .serializers import ProductSerializer, TableSerializer
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from fcm_django.models import FCMDevice
from django.views.generic import CreateView, UpdateView
from .forms import CreateClientForm
from django.http import HttpResponseRedirect


# Create your views here.
class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class TableList(ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


@api_view(["POST"])
def update_device_token(request):
    new_token = request.data.get("new_token")
    # Asegúrate de que el ID de usuario y el nuevo token estén presentes
    if not new_token:
        return Response({"status": "Missing token"}, status=400)

    try:
        device, created = FCMDevice.objects.get_or_create(
            device_id="E01", defaults={"device_id": "E01", "registration_id": new_token}
        )

        if not created:
            device.registration_id = new_token
            device.save()

        return Response({"status": "Token updated", "created": created})

    except device.DoesNotExist:
        return Response({"status": "User not found"}, status=404)


class ClientCreateView(CreateView):
    model = Client
    form_class = CreateClientForm
    template_name = "create-client.html"

    def get_success_url(self):
        order_id = self.request.session.get("current_order_id")
        return reverse("payment:money_payment", kwargs={"pk": order_id})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            return HttpResponseRedirect(self.get_success_url())
        self.object = None
        context = self.get_context_data(**kwargs)
        context["form"] = form
        return render(request, self.template_name, context)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = CreateClientForm
    template_name = "update-client.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        order_id = self.request.session.get("current_order_id")
        return reverse("payment:money_payment", kwargs={"pk": order_id})

    def form_valid(self, form):
        return super().form_valid(form)
