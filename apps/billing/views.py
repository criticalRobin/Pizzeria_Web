from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from apps.billing.models import Bill
from django.template.loader import render_to_string
from weasyprint import HTML
from apps.api.models import OrderDetails


# Create your views here.
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

    response = HttpResponse(result, content_type="application/pdf;")
    response["Content-Disposition"] = f"inline; filename=factura_{bill.pk}.pdf"
    return response
