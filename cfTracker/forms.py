from django import forms
from .models import *
from django.conf import settings


class ReceiptForm(forms.Form):
    image = forms.ImageField()
