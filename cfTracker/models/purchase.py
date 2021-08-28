from django.db import models
from django.utils import timezone
import secrets


class Purchase(models.Model):
    slug = models.CharField(
        default=lambda: secrets.token_urlsafe(10),
        unique=True,
        editable=False,
        blank=False,
        max_length=10
    )
    store = models.CharField(max_length=80)
    time = models.DateTimeField(auto_now=True)


class Item(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items', blank=False)
    item = models.CharField(blank=False, max_length=80)
    quantity = models.FloatField()