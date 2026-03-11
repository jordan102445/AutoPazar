import django_filters

from apps.listings.models import Listing


class ListingFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    year_min = django_filters.NumberFilter(field_name="year", lookup_expr="gte")
    year_max = django_filters.NumberFilter(field_name="year", lookup_expr="lte")
    mileage_min = django_filters.NumberFilter(field_name="mileage", lookup_expr="gte")
    mileage_max = django_filters.NumberFilter(field_name="mileage", lookup_expr="lte")
    city = django_filters.CharFilter(field_name="city__slug")
    brand = django_filters.CharFilter(field_name="brand__slug")
    car_model = django_filters.CharFilter(field_name="car_model__slug")

    class Meta:
        model = Listing
        fields = [
            "brand",
            "car_model",
            "fuel_type",
            "transmission",
            "body_type",
            "condition",
            "city",
            "price_min",
            "price_max",
            "year_min",
            "year_max",
            "mileage_min",
            "mileage_max",
        ]

