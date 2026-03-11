from django import forms
from django.core.exceptions import ValidationError

from apps.core.forms import TailwindFormMixin
from apps.core.validators import validate_phone_number

from .models import InquiryMessage


class InquiryForm(TailwindFormMixin, forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = InquiryMessage
        fields = ("sender_name", "sender_email", "sender_phone", "message")
        labels = {
            "sender_name": "Име и презиме",
            "sender_email": "Е-пошта",
            "sender_phone": "Телефон",
            "message": "Порака",
        }
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_sender_phone(self):
        phone = self.cleaned_data.get("sender_phone", "")
        if phone:
            validate_phone_number(phone)
        return phone

    def clean_website(self):
        value = self.cleaned_data.get("website")
        if value:
            raise ValidationError("Детектирана е несакана содржина.")
        return value
