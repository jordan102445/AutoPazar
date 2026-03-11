from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class ReportReason(models.TextChoices):
    FRAUD = "fraud", _("Сомнителен оглас / измама")
    DUPLICATE = "duplicate", _("Дупликат")
    WRONG_DATA = "wrong_data", _("Неточни податоци")
    OFFENSIVE = "offensive", _("Навредлива содржина")
    SOLD = "sold", _("Веќе продаден")
    OTHER = "other", _("Друго")


class ReportStatus(models.TextChoices):
    OPEN = "open", _("Отворена")
    REVIEWING = "reviewing", _("Во проверка")
    ACTIONED = "actioned", _("Преземено дејство")
    DISMISSED = "dismissed", _("Отфрлена")


class ListingReport(TimeStampedModel):
    listing = models.ForeignKey(
        "listings.Listing",
        on_delete=models.CASCADE,
        related_name="reports",
    )
    reporter = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="reports",
        blank=True,
        null=True,
    )
    reason = models.CharField(max_length=30, choices=ReportReason.choices)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=ReportStatus.choices, default=ReportStatus.OPEN)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="reviewed_reports",
        blank=True,
        null=True,
    )
    reviewed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Пријава за оглас")
        verbose_name_plural = _("Пријави за огласи")

    def __str__(self) -> str:
        return f"Report {self.id} for listing {self.listing_id}"


class AuditLog(TimeStampedModel):
    actor = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="audit_events",
        blank=True,
        null=True,
    )
    listing = models.ForeignKey(
        "listings.Listing",
        on_delete=models.SET_NULL,
        related_name="audit_logs",
        blank=True,
        null=True,
    )
    event_type = models.CharField(max_length=80)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Лог за активности")
        verbose_name_plural = _("Логови за активности")

    def __str__(self) -> str:
        return f"{self.event_type} ({self.created_at:%Y-%m-%d %H:%M})"
