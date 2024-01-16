import re
from xml.dom import ValidationErr
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator, EmailValidator
from decimal import Decimal
from django.core.exceptions import ValidationError


# Create your models here.
class Entity(models.Model):
    ruc = models.CharField(max_length=13, verbose_name="RUC", unique=True)
    commercial_name = models.CharField(max_length=50, verbose_name="Nombre Comercial")
    stablishement_address = models.CharField(
        max_length=50, verbose_name="Dirección Establecimiento"
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
        null=True,
        blank=True,
        verbose_name="Teléfono",
    )

    def __str__(self):
        return f"{self.commercial_name} - {self.ruc}"

    class Meta:
        verbose_name = "Entidad"
        verbose_name_plural = "Entidades"
        ordering = ["id"]


dni_regex = r"^\d{10}$"


def ecuadorian_dni_validator(dni):
    if len(dni) == 10:
        province = int(dni[0:2])
        if province >= 1 and province <= 24:
            last_digit = int(dni[9])
            even_sum = sum(int(dni[i]) for i in range(1, 9, 2))
            odd_sum = 0
            for i in range(0, 9, 2):
                odd_digit = int(dni[i]) * 2
                if odd_digit > 9:
                    odd_digit -= 9
                odd_sum += odd_digit
            total = even_sum + odd_sum
            first_digit = int(str(total)[0])
            next_ten = (first_digit + 1) * 10
            validator = next_ten - total
            if validator == 10:
                validator = 0
            if validator == last_digit:
                return 
            else:
                raise ValidationError(f"La cedula no existe, cambie el ultimo digito por {validator} para que su cedula sea aceptada")
                
        else:
            raise ValidationError('Provincia no encontrada')
    else:
        raise ValidationError('Su cedula no posee 10 digitos')


class Client(models.Model):
    dni = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10), ecuadorian_dni_validator],
        unique=True,
        null=True,
        blank=True,
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
        null=True,
        blank=True,
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
        null=True,
        blank=True,
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


class Category(models.Model):
    name = models.CharField(
        max_length=20, null=False, blank=False, verbose_name="Nombre"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


class Product(models.Model):
    name = models.CharField(
        max_length=20, null=False, blank=False, verbose_name="Nombre"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Categoría",
        null=True,
        blank=True,
        default=None,
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
