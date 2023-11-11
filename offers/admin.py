from django.contrib import admin
from orders.models import Order
from api.forms import OfferAdminForm
from django.forms import DateInput
from .models import (
    Company,
    Offer,
    OfferDate,
    Location,
    Category,
    SubCategory,
    Pictures,
    OfferDate,
    Feedbacks,
    DayOfWeek,
    Month,
)


class InlineDate(admin.StackedInline):
    model = OfferDate
    extra = 1


class OfferAdmin(admin.ModelAdmin):
    inlines = [InlineDate]


class OrderAdmin(admin.ModelAdmin):
    search_fields = ["id", "offer_id__title"]
    list_display = (
        "user_id",
        "offer",
        "redeemed",
        "coupons_ordered",
        "order_date",
        "is_gift",
        "is_active",
    )
    list_filter = ("is_active",)  # Add this line to filter by is_active field

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            obj.activate()  # Call the activate function when is_active is True
        obj.save()


admin.site.register(Order, OrderAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferDate)
admin.site.register(Location)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Company)
admin.site.register(Feedbacks)
admin.site.register(DayOfWeek)
admin.site.register(Month)
