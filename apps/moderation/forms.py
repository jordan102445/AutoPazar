from django import forms
from django.core.exceptions import ValidationError

from apps.core.forms import TailwindFormMixin
from .models import ListingReport


class ListingReportForm(TailwindFormMixin, forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ListingReport
        fields = ("reason", "description")
        labels = {
            "reason": "Причина",
            "description": "Опис",
        }
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}

    def clean_website(self):
        value = self.cleaned_data.get("website")
        if value:
            raise ValidationError("Детектирана е несакана содржина.")
        return value
