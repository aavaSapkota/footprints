from . import models
from . import forms
from django.core.files.images import ImageFile
from django.urls import reverse
from django.views import generic
from .csvReader import data, aliases
from .parseReceipt import parse_receipt


class HomePageView(generic.TemplateView):
    template_name = "index.html"


class UploadPageView(generic.edit.FormView):
    template_name = "upload.html"
    form_class = forms.ReceiptForm
    success_url = '/results/'

    def form_valid(self, form):
        # call parser, which returns data
        receipt_img = form.cleaned_data.get("image")
        store_name, items = parse_receipt(receipt_img.read())

        # create objects from the data
        p = models.Purchase.objects.create(store=store_name,receipt=receipt_img)
        p.save()

        for item_name, item_quantity in items.items():
            models.Item.objects.create(item=item_name, quantity=item_quantity,purchase=p)

        # redirect
        self.success_url = reverse('results', kwargs={'slug': p.slug})
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
        local_count = 0
        for item in purchase.items.all():
            i = {'item': item.item, 'quantity': item.quantity, 'emissions': 0}

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
                    local_count += 1
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
            i['emissions'] = round(i['emissions'], 5)
            context['items'].append(i)

        local_percent = local_count/len(purchase.items.all())
        global_percent = (1-local_percent)
        context['local_percent'] = int(round(local_percent, 2)*100)
        context['global_percent'] = int(round(global_percent, 2)*100)

        if local_percent < global_percent:
            context['local_ratio'] = int(round(local_percent / global_percent, 2)*100)
            context['global_ratio'] = 100
        elif local_percent > global_percent:
            context['local_ratio'] = 100
            context['global_ratio'] = int(round(global_percent / local_percent, 2)*100)
        else:
            context['local_ratio'] = context['global_ratio'] = 100

        context['emissions_land'] = emissions_land
        context['emissions_farm'] = emissions_farm
        context['emissions_feed'] = emissions_feed
        context['emissions_processing'] = emissions_processing
        context['emissions_transport'] = emissions_transport
        context['emissions_retail'] = emissions_retail
        context['emissions_packaging'] = emissions_packaging
        context['emissions'] = emissions_land + emissions_farm + emissions_feed + \
            emissions_processing + emissions_transport + \
            emissions_retail + emissions_packaging
        context['emissions'] = round(context['emissions'], 3)

        about = [
            {
                "title": "Total CO2 Released",
                "description": "The total CO2 released is calculated as the sum of the impact of producing the grocery item(according to OurWorldinData) and the impact of transporting the food from its place of origin to Toronto."
            },
            {
                "title": "Locally vs Globally Sourced",
                "description": "Place of origin has a small impact on the carbon footprint because most produce is transported by water, not air. Despite this, locally sourced goods generally have a lower carbon footprint."
            },
            {
                "title": "Kg of CO2 per Kg of Produce",
                "description": "This is the unit of measure used to describe the carbon 'footprint' or impact of an item. It is the CO2 equivalent in kilograms per kilogram of said item"
            }
        ]
        context['about'] = about

        return context
