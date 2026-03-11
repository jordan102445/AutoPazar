from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.urls import reverse_lazy

from apps.core.forms import TailwindFormMixin
from apps.core.models import City
from apps.core.validators import validate_image_file

from .choices import ListingStatus
from .models import CarBrand, CarModel, Listing, ListingImage


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        if not data:
            return []

        single_file_clean = super().clean
        files = data if isinstance(data, (list, tuple)) else [data]
        cleaned_files = []
        errors = []

        for uploaded_file in files:
            try:
                cleaned_files.append(single_file_clean(uploaded_file, initial))
            except ValidationError as exc:
                errors.extend(exc.error_list)

        if errors:
            raise ValidationError(errors)

        return cleaned_files


class ListingForm(TailwindFormMixin, forms.ModelForm):
    new_images = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={"accept": "image/*"}),
        label="Фотографии",
        help_text="Дозволени формати: JPG, PNG, WEBP. Максимум 8MB по слика.",
    )

    class Meta:
        model = Listing
        fields = (
            "title",
            "description",
            "price",
            "currency",
            "negotiable",
            "brand",
            "car_model",
            "trim",
            "year",
            "mileage",
            "fuel_type",
            "transmission",
            "body_type",
            "engine_size",
            "horsepower",
            "drive_type",
            "color",
            "condition",
            "city",
            "registered_until",
            "first_owner",
            "service_history",
            "imported",
            "number_of_doors",
            "vin",
            "show_vin",
            "show_phone",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 6}),
            "registered_until": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "title": "Наслов",
            "description": "Опис",
            "price": "Цена",
            "currency": "Валута",
            "negotiable": "По договор",
            "brand": "Марка",
            "car_model": "Модел",
            "trim": "Пакет / опрема",
            "year": "Година",
            "mileage": "Километража",
            "fuel_type": "Гориво",
            "transmission": "Менувач",
            "body_type": "Каросерија",
            "engine_size": "Зафатнина на мотор",
            "horsepower": "Коњски сили",
            "drive_type": "Погон",
            "color": "Боја",
            "condition": "Состојба",
            "city": "Град",
            "registered_until": "Регистриран до",
            "first_owner": "Прв сопственик",
            "service_history": "Сервисна историја",
            "imported": "Увезен",
            "number_of_doors": "Број на врати",
            "vin": "VIN број",
            "show_vin": "Прикажи VIN јавно",
            "show_phone": "Прикажи телефон",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["brand"].queryset = CarBrand.objects.filter(is_active=True)
        self.fields["city"].queryset = City.objects.filter(is_active=True)
        self.fields["car_model"].queryset = CarModel.objects.filter(is_active=True)
        self.fields["brand"].widget.attrs.update(
            {
                "hx-get": reverse_lazy("listings:model-options"),
                "hx-target": "#id_car_model",
                "hx-swap": "innerHTML",
            }
        )
        selected_brand = None
        if self.is_bound:
            brand_value = self.data.get("brand")
            if brand_value:
                selected_brand = brand_value
        elif self.instance.pk:
            selected_brand = self.instance.brand_id
        if selected_brand:
            self.fields["car_model"].queryset = CarModel.objects.filter(brand_id=selected_brand)

    def clean(self):
        cleaned = super().clean()
        brand = cleaned.get("brand")
        car_model = cleaned.get("car_model")
        if brand and car_model and car_model.brand_id != brand.id:
            raise ValidationError("Моделот мора да припаѓа на избраната марка.")
        return cleaned

    def clean_vin(self):
        vin = self.cleaned_data.get("vin", "").strip().upper()
        if vin and len(vin) != 17:
            raise ValidationError("VIN бројот мора да содржи 17 карактери.")
        return vin

    def clean_new_images(self):
        images = self.cleaned_data.get("new_images", [])
        for image in images:
            validate_image_file(image)
        return images


class ListingImageManageForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = ListingImage
        fields = ("alt_text", "sort_order", "is_cover")
        labels = {
            "alt_text": "Алт текст",
            "sort_order": "Редослед",
            "is_cover": "Насловна фотографија",
        }


ListingImageFormSet = inlineformset_factory(
    Listing,
    ListingImage,
    form=ListingImageManageForm,
    fields=("alt_text", "sort_order", "is_cover"),
    extra=0,
    can_delete=True,
)


class ListingFilterForm(TailwindFormMixin, forms.Form):
    keyword = forms.CharField(required=False, label="Клучен збор")
    brand = forms.ModelChoiceField(required=False, queryset=CarBrand.objects.filter(is_active=True), label="Марка")
    car_model = forms.ModelChoiceField(required=False, queryset=CarModel.objects.filter(is_active=True), label="Модел")
    price_min = forms.DecimalField(required=False, min_value=0, label="Цена од")
    price_max = forms.DecimalField(required=False, min_value=0, label="Цена до")
    year_min = forms.IntegerField(required=False, min_value=1950, label="Година од")
    year_max = forms.IntegerField(required=False, min_value=1950, label="Година до")
    mileage_min = forms.IntegerField(required=False, min_value=0, label="Километража од")
    mileage_max = forms.IntegerField(required=False, min_value=0, label="Километража до")
    fuel_type = forms.ChoiceField(required=False, label="Гориво", choices=[("", "Сите")] + list(Listing._meta.get_field("fuel_type").choices))
    transmission = forms.ChoiceField(required=False, label="Менувач", choices=[("", "Сите")] + list(Listing._meta.get_field("transmission").choices))
    body_type = forms.ChoiceField(required=False, label="Каросерија", choices=[("", "Сите")] + list(Listing._meta.get_field("body_type").choices))
    city = forms.ModelChoiceField(required=False, queryset=City.objects.filter(is_active=True), label="Град")
    condition = forms.ChoiceField(required=False, label="Состојба", choices=[("", "Сите")] + list(Listing._meta.get_field("condition").choices))
    ordering = forms.ChoiceField(
        required=False,
        label="Подреди по",
        choices=(
            ("newest", "Најнови"),
            ("oldest", "Најстари"),
            ("price_asc", "Цена: растечки"),
            ("price_desc", "Цена: опаѓачки"),
            ("mileage", "Километража"),
        ),
        initial="newest",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["brand"].widget.attrs.update(
            {
                "hx-get": reverse_lazy("listings:model-options"),
                "hx-target": "#id_car_model",
                "hx-swap": "innerHTML",
            }
        )
        brand = None
        if self.is_bound and self.data.get("brand"):
            brand = self.data.get("brand")
        elif self.initial.get("brand"):
            brand = self.initial["brand"]
        if brand:
            self.fields["car_model"].queryset = CarModel.objects.filter(brand_id=brand)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("price_min") and cleaned.get("price_max") and cleaned["price_min"] > cleaned["price_max"]:
            raise ValidationError("Минималната цена не може да биде поголема од максималната.")
        if cleaned.get("year_min") and cleaned.get("year_max") and cleaned["year_min"] > cleaned["year_max"]:
            raise ValidationError("Минималната година не може да биде поголема од максималната.")
        if cleaned.get("mileage_min") and cleaned.get("mileage_max") and cleaned["mileage_min"] > cleaned["mileage_max"]:
            raise ValidationError("Минималната километража не може да биде поголема од максималната.")
        return cleaned


class ListingStatusForm(TailwindFormMixin, forms.Form):
    action = forms.ChoiceField(
        label="Акција",
        choices=(
            ("publish", "Испрати на одобрување"),
            ("draft", "Зачувај како нацрт"),
            ("mark_sold", "Означи како продадено"),
            ("archive", "Архивирај"),
            ("reactivate", "Повторно активирај"),
            ("delete", "Избриши"),
        )
    )
