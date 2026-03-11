from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

from apps.listings.models import Listing

from ..models import Favorite
from .serializers import FavoriteSerializer


class FavoriteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Favorite.objects.filter(user=self.request.user)
            .select_related("listing", "listing__brand", "listing__car_model", "listing__city")
            .prefetch_related("listing__images")
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        listing = Listing.objects.active().get(pk=serializer.validated_data["listing_id"])
        favorite, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
        output = self.get_serializer(favorite)
        return Response(output.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
