from django.contrib import admin
from . import models
import django.db


class ItemInline(admin.TabularInline):
    fields = [
        'purchase',
        'item',
        'quantity',
    ]
    model = models.Item
    extra = 0


class PurchaseAdmin(admin.ModelAdmin):
    list_display = [
        'slug',
        'store',
        'time',
    ]
    fields = [
        'store',
        'receipt',
    ]
    inlines = [
        ItemInline
    ]


admin.site.register(models.Purchase, PurchaseAdmin)
