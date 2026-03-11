from rest_framework import serializers

from apps.listings.api.serializers import ListingCardSerializer

from ..models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    listing = ListingCardSerializer(read_only=True)
    listing_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Favorite
        fields = ("id", "listing", "listing_id", "created_at")
        read_only_fields = ("id", "created_at", "listing")
