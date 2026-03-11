from rest_framework import serializers

from ..models import CarBrand, CarModel, Listing, ListingImage


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ("id", "image", "alt_text", "sort_order", "is_cover")


class ListingCardSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="brand.name", read_only=True)
    car_model = serializers.CharField(source="car_model.name", read_only=True)
    city = serializers.CharField(source="city.name", read_only=True)
    seller_name = serializers.CharField(source="seller.profile.full_name", read_only=True)
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = (
            "id",
            "title",
            "slug",
            "price",
            "currency",
            "year",
            "mileage",
            "brand",
            "car_model",
            "city",
            "featured",
            "status",
            "cover_image",
            "seller_name",
            "created_at",
        )

    def get_cover_image(self, obj):
        image = obj.cover_image
        if not image:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(image.image.url) if request else image.image.url


class ListingDetailSerializer(ListingCardSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    description = serializers.CharField()
    seller = serializers.SerializerMethodField()
    public_vin = serializers.CharField(read_only=True)

    class Meta(ListingCardSerializer.Meta):
        fields = ListingCardSerializer.Meta.fields + (
            "description",
            "negotiable",
            "trim",
            "fuel_type",
            "transmission",
            "body_type",
            "engine_size",
            "horsepower",
            "drive_type",
            "color",
            "condition",
            "registered_until",
            "first_owner",
            "service_history",
            "imported",
            "number_of_doors",
            "public_vin",
            "show_phone",
            "view_count",
            "images",
            "seller",
        )

    def get_seller(self, obj):
        return {
            "id": obj.seller_id,
            "name": obj.seller.profile.full_name,
            "city": obj.seller.profile.city.name if obj.seller.profile.city else "",
            "phone_number": obj.seller.profile.phone_number if obj.show_phone else "",
        }


class ListingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = (
            "id",
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
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def create(self, validated_data):
        validated_data["seller"] = self.context["request"].user
        validated_data.setdefault("status", "draft")
        return super().create(validated_data)

    def validate_status(self, value):
        request = self.context.get("request")
        if request and not request.user.is_staff and value == "active":
            raise serializers.ValidationError("Само модератори можат директно да активираат огласи.")
        return value


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = ("id", "name", "slug")


class CarModelSerializer(serializers.ModelSerializer):
    brand = CarBrandSerializer(read_only=True)

    class Meta:
        model = CarModel
        fields = ("id", "name", "slug", "brand")
