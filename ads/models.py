from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=1000)
    author = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=500)
    is_published = models.BooleanField()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)