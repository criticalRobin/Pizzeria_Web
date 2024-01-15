from django.forms import ModelForm
from .models import OrderDetails


class UpdateOrderDetailsForm(ModelForm):
    class Meta:
        model = OrderDetails
        fields = ["detail_status"]
        labels = {"detail_status": "Estado del platillo"}
