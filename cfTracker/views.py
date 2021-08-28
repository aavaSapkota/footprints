from . import models
from django.views import generic

class HomePageView(generic.TemplateView):

    template_name = "index.html"

class UploadPageView(generic.TemplateView):

    template_name = "upload.html"

class ResultsPageView(generic.TemplateView):

    template_name = "results.html"
