from rest_framework import mixins, permissions, viewsets

from apps.core.utils import get_client_ip

from ..models import AuditLog, ListingReport
from .serializers import ListingReportSerializer


class ListingReportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ListingReportSerializer

    def get_permissions(self):
        if self.action == "list":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return ListingReport.objects.select_related("listing", "reporter")
        return ListingReport.objects.filter(reporter=self.request.user).select_related("listing")

    def perform_create(self, serializer):
        reporter = self.request.user if self.request.user.is_authenticated else None
        report = serializer.save(
            reporter=reporter,
            ip_address=get_client_ip(self.request),
        )
        AuditLog.objects.create(
            actor=reporter,
            listing=report.listing,
            event_type="listing_reported",
            ip_address=report.ip_address,
            metadata={"reason": report.reason, "report_id": report.pk},
        )
