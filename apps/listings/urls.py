from django.urls import path

from .views import (
    BrandModelOptionsView,
    ListingCreateView,
    ListingDetailView,
    ListingListView,
    ListingStatusUpdateView,
    ListingUpdateView,
)

app_name = "listings"

urlpatterns = [
    path("", ListingListView.as_view(), name="list"),
    path("nov/", ListingCreateView.as_view(), name="create"),
    path("modeli/", BrandModelOptionsView.as_view(), name="model-options"),
    path("<slug:slug>/", ListingDetailView.as_view(), name="detail"),
    path("<slug:slug>/izmeni/", ListingUpdateView.as_view(), name="update"),
    path("<slug:slug>/status/", ListingStatusUpdateView.as_view(), name="status"),
]

