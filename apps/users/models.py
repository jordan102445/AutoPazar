from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel
from apps.core.validators import validate_phone_number

from .managers import UserManager


def user_profile_upload_to(instance, filename):
    return f"profiles/{instance.user_id}/{filename}"


class User(AbstractUser):
    username = None
    email = models.EmailField(_("е-пошта"), unique=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def get_display_name(self) -> str:
        if hasattr(self, "profile") and self.profile.full_name:
            return self.profile.full_name
        return self.email


class SellerType(models.TextChoices):
    PRIVATE = "private", _("Приватен")
    DEALERSHIP = "dealership", _("Автосалон")


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=180)
    phone_number = models.CharField(max_length=32, validators=[validate_phone_number])
    city = models.ForeignKey(
        "core.City",
        on_delete=models.SET_NULL,
        related_name="residents",
        null=True,
        blank=True,
    )
    seller_type = models.CharField(
        max_length=20,
        choices=SellerType.choices,
        default=SellerType.PRIVATE,
    )
    profile_image = models.ImageField(upload_to=user_profile_upload_to, blank=True, null=True)
    bio = models.TextField(blank=True)

    class Meta:
        verbose_name = _("Кориснички профил")
        verbose_name_plural = _("Кориснички профили")

    def __str__(self) -> str:
        return self.full_name

    @property
    def avatar_url(self):
        if self.profile_image:
            return self.profile_image.url
        return static("img/avatar-placeholder.svg")
