from django.db import models
from django.utils import timezone
import secrets


class Purchase(models.Model):
    slug = models.CharField(
        default=lambda: secrets.token_urlsafe(10),
        unique=True,
        editable=False,
        blank=False
    )
    store = models.CharField()
    time = models.DateTimeField(auto_now=True)


class Item(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items', blank=False)
    item = models.CharField(blank=False)
    quantity = models.FloatField()