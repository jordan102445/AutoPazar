from rest_framework import serializers

from ..models import ListingReport


class ListingReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingReport
        fields = ("id", "listing", "reason", "description", "status", "created_at")
        read_only_fields = ("id", "status", "created_at")
