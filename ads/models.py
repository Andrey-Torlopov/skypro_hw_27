from django.core.validators import (MaxLengthValidator, MinLengthValidator)
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(
        max_length=10, validators=[
            MinLengthValidator(5),
            MaxLengthValidator(10)
        ],
        null=True,
        blank=True,
        default=None)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.name


class Ad(models.Model):
    name = models.CharField(max_length=1000, null=False, validators=[MinLengthValidator(10)])
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    price = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='ad_img/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self) -> str:
        return self.name


class Selection(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    items = models.ManyToManyField(Ad)

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"

    def __str__(self) -> str:
        return self.name
