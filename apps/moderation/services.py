import logging

from apps.core.utils import get_client_ip

from .models import AuditLog, ListingReport

audit_logger = logging.getLogger("audit")


def create_listing_report(listing, form, request):
    report = form.save(commit=False)
    report.listing = listing
    report.reporter = request.user if request.user.is_authenticated else None
    report.ip_address = get_client_ip(request)
    report.save()
    AuditLog.objects.create(
        actor=request.user if request.user.is_authenticated else None,
        listing=listing,
        event_type="listing_reported",
        ip_address=report.ip_address,
        metadata={"reason": report.reason, "report_id": report.pk},
    )
    audit_logger.info(
        "listing_reported listing_id=%s report_id=%s reason=%s ip=%s",
        listing.pk,
        report.pk,
        report.reason,
        report.ip_address,
    )
    return report
