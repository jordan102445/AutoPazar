from rest_framework import serializers

from ..models import InquiryMessage


class InquiryMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InquiryMessage
        fields = (
            "id",
            "listing",
            "sender_name",
            "sender_email",
            "sender_phone",
            "message",
            "status",
            "created_at",
        )
        read_only_fields = ("id", "status", "created_at")
