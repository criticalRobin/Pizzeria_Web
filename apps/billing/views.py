from typing import Any
from django.core.mail import EmailMessage, BadHeaderError
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from apps.billing.models import Bill
from django.template.loader import render_to_string
from weasyprint import HTML
from apps.api.models import OrderDetails
from django.views.generic import ListView


# Create your views here.
class BillListView(ListView):
    model = Bill
    template_name = "bill_list.html"
    context_object_name = "bills"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return super().get_context_data(**kwargs)


def bill_pdf(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    entity = bill.entity
    payment = bill.payment
    order = payment.order
    order_details = OrderDetails.objects.filter(order=order)
    client = payment.client

    context = {
        "bill": bill,
        "entity": entity,
        "payment": payment,
        "order": order,
        "order_details": order_details,
        "client": client,
    }

    html_string = render_to_string("bill.html", context)

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf(presentational_hints=True)

    email = EmailMessage(
        subject="Factura Pizzeria la Cigarra",
        body="Aquí está la factura de tu reciente orden.",
        from_email="lacigarrasw@gmail.com",
        to=[client.email],
    )

    email.attach(f"factura_{bill.pk}.pdf", result, "application/pdf")

    try:
        email.send()
        print("El correo electrónico se ha enviado correctamente.")
    except BadHeaderError:
        print("Error en los encabezados del correo electrónico.")
        return HttpResponse("Invalid header found.")
    except Exception as e:
        print(f"Ocurrió un error al enviar el correo: {e}")
        return HttpResponse("Email could not be sent")

    response = HttpResponse(result, content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename=factura_{bill.pk}.pdf"
    return response
