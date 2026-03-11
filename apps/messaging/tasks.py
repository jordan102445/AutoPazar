from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import InquiryMessage


@shared_task
def send_inquiry_notification(inquiry_id):
    try:
        inquiry = InquiryMessage.objects.select_related("listing", "seller").get(pk=inquiry_id)
    except InquiryMessage.DoesNotExist:
        return

    subject = f"Нова порака за {inquiry.listing.title}"
    body = render_to_string("emails/inquiry_notification.txt", {"inquiry": inquiry})
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [inquiry.seller.email], fail_silently=True)
