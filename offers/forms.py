from django.contrib import admin
from django import forms
from django.forms import DateInput
from .models import Offer, OfferDate




class OfferDateForm(forms.ModelForm):
    class Meta:
        model = OfferDate
        widgets = {
            'startdate': DateInput(attrs={'type': 'date'}),
            'enddate': DateInput(attrs={'type': 'date'}),
        }