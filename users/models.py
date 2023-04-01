from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


def check_children_age(value: date) -> None:
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 9:
        raise ValidationError("Пользователь не может быть младше 9 лет.")


def not_rambler_mail(value: str) -> None:
    domain = value.split("@")[1].split(".")[0]
    if domain.lower() == 'rambler.ru':
        raise ValidationError('Нельзя регистрироваться с rambler.ru.')


class Location(models.Model):
    name = models.CharField(max_length=150, unique=True)
    lat = models.DecimalField(
        max_digits=8, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(
        max_digits=8, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self) -> str:
        return self.name


class UserRole(models.TextChoices):
    MEMBER = 'member', _("member")
    MODERATOR = 'moderator', _("moderator")
    ADMIN = 'admin', _("admin")


class User(AbstractUser):
    role = models.CharField(
        max_length=10, choices=UserRole.choices, default='member')
    location = models.ManyToManyField(Location, null=True, blank=True)
    birth_date = models.DateField(null=True, validators=[check_children_age])
    email = models.CharField(max_length=50, unique=True, validators=[not_rambler_mail])

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self) -> str:
        return self.username
