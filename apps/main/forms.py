from django import forms
from .models import Client


class CreateClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs["class"] = "form-control"
            form.field.widget.attrs["autocomplete"] = "off"
            form.field.widget.attrs["placeholder"] = (
                form.label[0].capitalize() + form.label[1:].lower()
            )
        self.fields["dni"].widget.attrs["autofocus"] = True

    class Meta:
        model = Client
        fields = "__all__"
        labels = {
            "dni": "Identificación",
            "name": "Nombre",
            "surname": "Apellido",
            "address": "Dirección",
            "phone": "Teléfono",
            "email": "Email",
            "gender": "Género",
        }
