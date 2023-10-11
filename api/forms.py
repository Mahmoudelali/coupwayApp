from django import forms
from offers.models import Offer
from django.contrib import admin


class OfferAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "coupons",
        ...,
    )  # Add other fields you want to display in the list view


class OfferAdminForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            "location",
            "company",
            "title",
            "coupons",
            "working",
            "main_picture",
            "highlights",
            "compensations",
            "fine_print",
            "description",
            "old_price",
            "new_price",
            "category",
            "subcategories",
            "isVip",
            "is_unique",
            "days_of_week",
            "months",
            "start_time",
            "end_time",
        ]
