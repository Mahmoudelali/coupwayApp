from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from offers.models import DayOfWeek, Month, Offer , OfferDate


class MultiSelectDatepicker(forms.ModelMultipleChoiceField):
    widget = FilteredSelectMultiple("Days of Week", is_stacked=False)

    def label_from_instance(self, obj):
        return obj.get_name_display()


class TimePicker(forms.TimeInput):
    input_type = "time"


class OfferAdminForm(forms.ModelForm):
    days_of_week = MultiSelectDatepicker(queryset=DayOfWeek.objects.all())
    months = MultiSelectDatepicker(queryset=Month.objects.all())
    start_time = forms.TimeField(widget=TimePicker)
    end_time = forms.TimeField(widget=TimePicker)

    class Meta:
        model = OfferDate
        fields = "__all__"
