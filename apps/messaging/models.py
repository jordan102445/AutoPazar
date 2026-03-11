from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class InquiryStatus(models.TextChoices):
    NEW = "new", _("Нова")
    REPLIED = "replied", _("Одговорена")
    ARCHIVED = "archived", _("Архивирана")


class InquiryMessage(TimeStampedModel):
    listing = models.ForeignKey(
        "listings.Listing",
        on_delete=models.CASCADE,
        related_name="inquiries",
    )
    seller = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="received_inquiries",
    )
    sender = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="sent_inquiries",
        blank=True,
        null=True,
    )
    sender_name = models.CharField(max_length=180)
    sender_email = models.EmailField()
    sender_phone = models.CharField(max_length=32, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=InquiryStatus.choices, default=InquiryStatus.NEW)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True)
    is_spam = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Порака")
        verbose_name_plural = _("Пораки")

    def __str__(self) -> str:
        return f"Inquiry {self.id} for {self.listing_id}"
