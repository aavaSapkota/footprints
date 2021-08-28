from . import models
from . import forms
from django.views import generic
from .csvReader import data, aliases


class HomePageView(generic.TemplateView):
    template_name = "index.html"


class UploadPageView(generic.edit.FormView):
    template_name = "upload.html"
    form_class = forms.ReceiptForm
    success_url = '/'

    def form_valid(self, form):
        # call parser with receipt path
        # (form.cleaned_data.get("image").read())
        return super().form_valid(form)


class ResultsPageView(generic.TemplateView):
    template_name = "results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = context['slug']

        purchase = models.Purchase.objects.get(slug=slug)
        context['purchase'] = purchase

        emissions_land = 0
        emissions_farm = 0
        emissions_feed = 0
        emissions_processing = 0
        emissions_transport = 0
        emissions_retail = 0
        emissions_packaging = 0

        context['items'] = []
        for item in purchase.items.all():
            i = {}
            i['item'] = item.item
            i['quantity'] = item.quantity
            i['emissions'] = 0

            if item.item not in data.keys():
                item_data = data[aliases[item.item]]
            else:
                item_data = data[item.item]

            i['emissions'] += float(item_data['food_emissions_land_use']
                                    ) * item.quantity
            emissions_land += float(
                item_data['food_emissions_land_use']) * item.quantity
            i['emissions'] += float(item_data['food_emissions_farm']
                                    ) * item.quantity
            emissions_farm += float(
                item_data['food_emissions_farm']) * item.quantity
            i['emissions'] += float(item_data['food_emissions_animal_feed']
                                    ) * item.quantity
            emissions_feed += float(
                item_data['food_emissions_animal_feed']) * item.quantity
            i['emissions'] += float(item_data['food_emissions_processing']
                                    ) * item.quantity
            emissions_processing += float(
                item_data['food_emissions_processing']) * item.quantity
            i['emissions'] += float(item_data['food_emissions_retail']
                                    ) * item.quantity
            emissions_retail += float(
                item_data['food_emissions_retail']) * item.quantity
            i['emissions'] += float(item_data['food_emissions_packaging']
                                    ) * item.quantity
            emissions_packaging += float(
                item_data['food_emissions_packaging']) * item.quantity

            if len(item_data['source']) > 0:
                i['local'] = item_data['is_local'] == 'true'
                if i['local']:
                    i['emissions'] += 0.000060 * item.quantity * \
                        float(item_data['distance'])
                    emissions_transport += 0.000060 * \
                        item.quantity * float(item_data['distance'])
                else:
                    i['emissions'] += 0.000025 * item.quantity * \
                        float(item_data['distance'])
                    emissions_transport += 0.000025 * \
                        item.quantity * float(item_data['distance'])
            else:
                i['emissions'] += float(
                    item_data['food_emissions_transport']) * item.quantity
                emissions_transport += float(
                    item_data['food_emissions_transport']) * item.quantity
                i['local'] = False

            context['items'].append(i)

        context['emissions_land'] = emissions_land
        context['emissions_farm'] = emissions_farm
        context['emissions_feed'] = emissions_feed
        context['emissions_processing'] = emissions_processing
        context['emissions_transport'] = emissions_transport
        context['emissions_retail'] = emissions_retail
        context['emissions_packaging'] = emissions_packaging
        context['emissions'] = emissions_land + emissions_farm + emissions_feed + \
            emissions_processing + emissions_transport + emissions_retail + emissions_packaging

        return context
