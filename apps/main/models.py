import re
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator, EmailValidator
from decimal import Decimal

# Create your models here.
dni_regex = r"^\d{10}$"


def ecuadorian_dni_validator(dni):
    if re.match(dni_regex, dni):
        province = int(dni[0:2])
        if province >= 1 and province <= 24:
            return True
    return False


class Client(models.Model):
    dni = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10), ecuadorian_dni_validator],
        unique=True,
        null=False,
        blank=False,
        verbose_name="Cédula",
    )
    name = models.CharField(
        max_length=20,
        validators=[RegexValidator(r"^[a-zA-Z]*$", "Solo se permiten letras")],
        null=False,
        blank=False,
        verbose_name="Nombre",
    )
    surname = models.CharField(
        max_length=20,
        validators=[RegexValidator(r"^[a-zA-Z]*$", "Solo se permiten letras")],
        null=False,
        blank=False,
        verbose_name="Apellido",
    )
    address = models.CharField(
        max_length=35,
        validators=[
            RegexValidator(r"^[A-Za-z0-9\s]+$", "No se permiten caracteres especiales")
        ],
        null=False,
        blank=False,
        verbose_name="Dirección",
    )

    phone_regex = r"^[0-9]+$"
    phone_validator = RegexValidator(
        regex=phone_regex,
        message="El número de teléfono debe contener solo números.",
        code="invalid_phone",
    )
    phone_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[MinLengthValidator(10), phone_validator],
        verbose_name="Teléfono",
    )
    email = models.CharField(
        max_length=40,
        unique=True,
        null=True,
        blank=True,
        validators=[EmailValidator],
        verbose_name="Correo electrónico",
    )

    GENDER_CHOICES = [
        ("M", "Masculino"),
        ("F", "Femenino"),
        ("O", "Otro"),
    ]
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default="M", verbose_name="Género"
    )

    def __str__(self):
        return self.name + " " + self.surname

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Table(models.Model):
    chairs_number = models.IntegerField(default=1, verbose_name="Número de sillas")
    available = models.BooleanField(default=True, verbose_name="Disponible")

    def __str__(self):
        return "Mesa " + str(self.id)

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"


class Product(models.Model):
    name = models.CharField(
        max_length=20, null=False, blank=False, verbose_name="Nombre"
    )
    stock = models.PositiveIntegerField(
        default=0, null=True, blank=True, verbose_name="Stock"
    )
    unit_price = models.DecimalField(
        default=0.00, max_digits=9, decimal_places=2, verbose_name="Precio unitario"
    )

    IVA_CHOICES = [
        ("12.00", "12.00"),
        ("0.00", "0.00"),
    ]
    iva = models.CharField(
        max_length=5, choices=IVA_CHOICES, default="0.00", verbose_name="IVA"
    )
    sale_price = models.DecimalField(
        default=0.00, max_digits=9, decimal_places=2, verbose_name="Precio de venta"
    )
    description = models.CharField(
        max_length=35, null=False, blank=False, verbose_name="Descripción"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def save(self, *args, **kwargs):
        self.sale_price = self.unit_price + (
            self.unit_price * (Decimal(self.iva) * Decimal(0.01))
        )
        super().save(*args, **kwargs)
