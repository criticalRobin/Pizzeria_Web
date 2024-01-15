from django import forms
from .models import Payment


class CreatePaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Payment
        fields = ["client"]
