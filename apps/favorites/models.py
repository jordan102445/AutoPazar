from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class Favorite(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="favorites")
    listing = models.ForeignKey("listings.Listing", on_delete=models.CASCADE, related_name="favorites")

    class Meta:
        unique_together = ("user", "listing")
        ordering = ["-created_at"]
        verbose_name = _("Омилен оглас")
        verbose_name_plural = _("Омилени огласи")

    def __str__(self) -> str:
        return f"{self.user_id}:{self.listing_id}"
