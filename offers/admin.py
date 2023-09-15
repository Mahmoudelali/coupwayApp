from django.contrib import admin
from .models import (
    Company,
    Offer,
    Location,
    Category,
    SubCategory,
    Pictures,
    OfferDate,
    Feedbacks,
)
from orders.models import Order
from api.forms import OfferAdminForm


class OfferAdmin(admin.ModelAdmin):
    form = OfferAdminForm


admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferDate)
admin.site.register(Location)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Pictures)
admin.site.register(Company)
admin.site.register(Feedbacks)
admin.site.register(Order)
