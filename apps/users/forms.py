from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import transaction

from apps.core.forms import TailwindFormMixin
from apps.core.models import City

from .models import UserProfile

User = get_user_model()


class UserRegistrationForm(TailwindFormMixin, UserCreationForm):
    email = forms.EmailField(label="Е-пошта")
    full_name = forms.CharField(max_length=180, label="Име и презиме")
    phone_number = forms.CharField(max_length=32, label="Телефонски број")
    city = forms.ModelChoiceField(queryset=City.objects.filter(is_active=True), required=False, label="Град")

    class Meta:
        model = User
        fields = ("email", "full_name", "phone_number", "city", "password1", "password2")

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_active = True
        if commit:
            user.save()
            profile = user.profile
            profile.full_name = self.cleaned_data["full_name"]
            profile.phone_number = self.cleaned_data["phone_number"]
            profile.city = self.cleaned_data["city"]
            profile.save()
        return user


class EmailAuthenticationForm(TailwindFormMixin, AuthenticationForm):
    username = forms.EmailField(label="Е-пошта")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].label = "Лозинка"


class UserProfileForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("full_name", "phone_number", "city", "profile_image", "bio")
        labels = {
            "full_name": "Име и презиме",
            "phone_number": "Телефонски број",
            "city": "Град",
            "profile_image": "Профилна слика",
            "bio": "Краток опис",
        }
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }
