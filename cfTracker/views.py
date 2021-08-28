from .models import *
from django.views import generic

class HomePageView(TemplateView):

    template_name = "index.html"
