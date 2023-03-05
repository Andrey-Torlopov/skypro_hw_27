from django.db import models
from django.utils.translation import gettext_lazy as _


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


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.CharField(
        max_length=10, choices=UserRole.choices, default='member')
    age = models.PositiveSmallIntegerField()
    location = models.ManyToManyField(Location, null=True, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self) -> str:
        return self.username
