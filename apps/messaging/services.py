import logging

from apps.core.utils import get_client_ip

from .models import InquiryMessage
from .tasks import send_inquiry_notification

audit_logger = logging.getLogger("audit")


def create_inquiry(listing, form, request):
    inquiry = form.save(commit=False)
    inquiry.listing = listing
    inquiry.seller = listing.seller
    inquiry.sender = request.user if request.user.is_authenticated else None
    inquiry.ip_address = get_client_ip(request)
    inquiry.user_agent = request.META.get("HTTP_USER_AGENT", "")[:255]
    if inquiry.sender and inquiry.sender == listing.seller:
        raise ValueError("Не можете да контактирате за сопствен оглас.")
    inquiry.save()
    send_inquiry_notification.delay(inquiry.pk)
    audit_logger.info(
        "inquiry_created listing_id=%s inquiry_id=%s ip=%s",
        listing.pk,
        inquiry.pk,
        inquiry.ip_address,
    )
    return inquiry
