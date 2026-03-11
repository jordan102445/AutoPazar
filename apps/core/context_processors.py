from apps.core.models import City
from apps.messaging.models import InquiryMessage, InquiryStatus


def site_context(request):
    new_inquiry_count = 0
    if request.user.is_authenticated:
        new_inquiry_count = InquiryMessage.objects.filter(
            seller=request.user,
            status=InquiryStatus.NEW,
        ).count()

    return {
        "site_name": "AutoPazar",
        "site_tagline": "Купување и продажба на автомобили во Македонија",
        "nav_cities": City.objects.filter(is_active=True),
        "new_inquiry_count": new_inquiry_count,
    }
