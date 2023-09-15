from django import forms
from offers.models import Offer


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
        ]
