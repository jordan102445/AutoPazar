from rest_framework import serializers

from apps.listings.models import Listing
from apps.listings.api.serializers import ListingCardSerializer

from ..models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    city = serializers.StringRelatedField()

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "email",
            "full_name",
            "phone_number",
            "city",
            "seller_type",
            "bio",
            "profile_image",
            "created_at",
        )
        read_only_fields = ("id", "email", "created_at")


class SellerProfileSerializer(UserProfileSerializer):
    active_listings = serializers.SerializerMethodField()

    class Meta(UserProfileSerializer.Meta):
        fields = UserProfileSerializer.Meta.fields + ("active_listings",)

    def get_active_listings(self, obj):
        listings = (
            Listing.objects.active()
            .filter(seller=obj.user)
            .select_related("brand", "car_model", "city")
            .prefetch_related("images")[:10]
        )
        return ListingCardSerializer(listings, many=True, context=self.context).data
