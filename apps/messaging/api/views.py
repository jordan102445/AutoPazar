from rest_framework import exceptions, mixins, permissions, viewsets

from apps.core.utils import get_client_ip
from apps.listings.models import Listing

from ..models import InquiryMessage
from .serializers import InquiryMessageSerializer


class InquiryMessageViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = InquiryMessageSerializer

    def get_permissions(self):
        if self.action == "list":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return InquiryMessage.objects.filter(seller=self.request.user).select_related("listing", "sender")

    def perform_create(self, serializer):
        listing = Listing.objects.active().get(pk=self.request.data.get("listing"))
        sender = self.request.user if self.request.user.is_authenticated else None
        if sender and sender == listing.seller:
            raise exceptions.PermissionDenied("Не можете да испратите порака за сопствен оглас.")
        serializer.save(
            listing=listing,
            seller=listing.seller,
            sender=sender,
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get("HTTP_USER_AGENT", "")[:255],
        )
