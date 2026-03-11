from rest_framework import mixins, permissions, viewsets

from ..models import Listing
from ..selectors import owner_listing_queryset
from .filters import ListingFilter
from .serializers import ListingCardSerializer, ListingDetailSerializer, ListingWriteSerializer


class ListingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Listing.objects.active()
        .select_related("brand", "car_model", "city", "seller", "seller__profile")
        .prefetch_related("images")
    )
    lookup_field = "slug"
    filterset_class = ListingFilter
    search_fields = ("title", "description", "brand__name", "car_model__name")
    ordering_fields = ("created_at", "price", "mileage", "year")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ListingDetailSerializer
        return ListingCardSerializer


class MyListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingWriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        return owner_listing_queryset(self.request.user)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
