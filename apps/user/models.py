import re
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

# Create your models here.
dni_regex = r"^\d{10}$"


def ecuadorian_dni_validator(dni):
    if re.match(dni_regex, dni):
        province = int(dni[0:2])
        if province >= 1 and province <= 24:
            return True
    return False


class User(AbstractUser):
    dni = models.CharField(
        max_length=10,
        unique=True,
        validators=[ecuadorian_dni_validator],
        verbose_name="Cédula",
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

    ROLE_CHOICES = [
        ("admin", "Administrador"),
        ("waiter", "Mesero"),
        ("cashier", "Cajero"),
        ("chef", "Cocinero"),
    ]
    employee_role = models.CharField(
        max_length=7, choices=ROLE_CHOICES, verbose_name="Rol"
    )
