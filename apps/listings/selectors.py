from django.db.models import Q

from .choices import ListingStatus
from .models import Listing


LISTING_ORDERING_MAP = {
    "newest": ("-featured", "-published_at", "-created_at"),
    "oldest": ("published_at", "created_at"),
    "price_asc": ("price", "-created_at"),
    "price_desc": ("-price", "-created_at"),
    "mileage": ("mileage", "-created_at"),
}


def listings_base_queryset():
    return (
        Listing.objects.active()
        .select_related("brand", "car_model", "city", "seller", "seller__profile")
        .prefetch_related("images")
    )


def listing_detail_queryset(user=None):
    queryset = (
        Listing.all_objects.select_related("brand", "car_model", "city", "seller", "seller__profile")
        .prefetch_related("images")
        .filter(deleted_at__isnull=True)
    )
    if user and user.is_authenticated:
        return queryset.filter(Q(status=ListingStatus.ACTIVE) | Q(seller=user) | Q(status=ListingStatus.SOLD))
    return queryset.filter(status__in=[ListingStatus.ACTIVE, ListingStatus.SOLD])


def filter_listings(cleaned_data):
    queryset = listings_base_queryset()

    keyword = cleaned_data.get("keyword")
    if keyword:
        queryset = queryset.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))

    if cleaned_data.get("brand"):
        queryset = queryset.filter(brand=cleaned_data["brand"])
    if cleaned_data.get("car_model"):
        queryset = queryset.filter(car_model=cleaned_data["car_model"])
    if cleaned_data.get("city"):
        queryset = queryset.filter(city=cleaned_data["city"])
    if cleaned_data.get("fuel_type"):
        queryset = queryset.filter(fuel_type=cleaned_data["fuel_type"])
    if cleaned_data.get("transmission"):
        queryset = queryset.filter(transmission=cleaned_data["transmission"])
    if cleaned_data.get("body_type"):
        queryset = queryset.filter(body_type=cleaned_data["body_type"])
    if cleaned_data.get("condition"):
        queryset = queryset.filter(condition=cleaned_data["condition"])
    if cleaned_data.get("price_min") is not None:
        queryset = queryset.filter(price__gte=cleaned_data["price_min"])
    if cleaned_data.get("price_max") is not None:
        queryset = queryset.filter(price__lte=cleaned_data["price_max"])
    if cleaned_data.get("year_min") is not None:
        queryset = queryset.filter(year__gte=cleaned_data["year_min"])
    if cleaned_data.get("year_max") is not None:
        queryset = queryset.filter(year__lte=cleaned_data["year_max"])
    if cleaned_data.get("mileage_min") is not None:
        queryset = queryset.filter(mileage__gte=cleaned_data["mileage_min"])
    if cleaned_data.get("mileage_max") is not None:
        queryset = queryset.filter(mileage__lte=cleaned_data["mileage_max"])

    ordering = cleaned_data.get("ordering") or "newest"
    return queryset.order_by(*LISTING_ORDERING_MAP.get(ordering, LISTING_ORDERING_MAP["newest"]))


def owner_listing_queryset(user):
    return (
        Listing.all_objects.filter(seller=user, deleted_at__isnull=True)
        .select_related("brand", "car_model", "city")
        .prefetch_related("images")
    )
