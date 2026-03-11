from decimal import Decimal

from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import F
from django.template.defaultfilters import truncatechars
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.core.models import SoftDeleteModel, TimeStampedModel
from apps.core.validators import validate_image_file

from .choices import (
    BodyType,
    Currency,
    DriveType,
    FuelType,
    ListingCondition,
    ListingStatus,
    TransmissionType,
)


def listing_image_upload_to(instance, filename):
    return f"listings/{instance.listing_id}/{filename}"


class CarBrand(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Марка на возило")
        verbose_name_plural = _("Марки на возила")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CarModel(TimeStampedModel):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("brand", "name")
        ordering = ["brand__name", "name"]
        verbose_name = _("Модел на возило")
        verbose_name_plural = _("Модели на возила")

    def __str__(self) -> str:
        return f"{self.brand.name} {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ListingQuerySet(models.QuerySet):
    def public(self):
        return self.filter(
            status__in=[ListingStatus.ACTIVE, ListingStatus.SOLD],
            deleted_at__isnull=True,
        )

    def active(self):
        return self.filter(status=ListingStatus.ACTIVE, deleted_at__isnull=True)

    def visible_for_owner(self, user):
        if user.is_staff:
            return self.filter(deleted_at__isnull=True)
        return self.filter(seller=user, deleted_at__isnull=True)


class Listing(SoftDeleteModel):
    seller = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="listings",
    )
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.EUR)
    negotiable = models.BooleanField(default=False)
    brand = models.ForeignKey(CarBrand, on_delete=models.PROTECT, related_name="listings")
    car_model = models.ForeignKey(CarModel, on_delete=models.PROTECT, related_name="listings")
    trim = models.CharField(max_length=120, blank=True)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1950), MaxValueValidator(timezone.now().year + 1)]
    )
    mileage = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=20, choices=FuelType.choices)
    transmission = models.CharField(max_length=20, choices=TransmissionType.choices)
    body_type = models.CharField(max_length=20, choices=BodyType.choices)
    engine_size = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal("0.6")), MaxValueValidator(Decimal("9.0"))],
    )
    horsepower = models.PositiveSmallIntegerField(blank=True, null=True)
    drive_type = models.CharField(max_length=20, choices=DriveType.choices, blank=True)
    color = models.CharField(max_length=60)
    condition = models.CharField(max_length=20, choices=ListingCondition.choices)
    city = models.ForeignKey("core.City", on_delete=models.PROTECT, related_name="listings")
    registered_until = models.DateField(blank=True, null=True)
    first_owner = models.BooleanField(blank=True, null=True)
    service_history = models.BooleanField(blank=True, null=True)
    imported = models.BooleanField(blank=True, null=True)
    number_of_doors = models.PositiveSmallIntegerField(blank=True, null=True)
    vin = models.CharField(max_length=17, blank=True)
    show_vin = models.BooleanField(default=False)
    show_phone = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=ListingStatus.choices, default=ListingStatus.DRAFT)
    featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)

    objects = ListingQuerySet.as_manager()
    all_objects = ListingQuerySet.as_manager()

    class Meta:
        ordering = ["-featured", "-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["brand", "car_model"]),
            models.Index(fields=["city", "year"]),
            models.Index(fields=["price", "created_at"]),
        ]
        verbose_name = _("Оглас")
        verbose_name_plural = _("Огласи")

    def __str__(self) -> str:
        return truncatechars(self.title, 50)

    @property
    def display_price(self) -> str:
        return f"{self.price:,.0f} {self.currency}".replace(",", " ")

    @property
    def public_vin(self) -> str:
        if self.show_vin:
            return self.vin
        if not self.vin:
            return ""
        return f"{self.vin[:3]}********{self.vin[-4:]}"

    @property
    def cover_image(self):
        return self.images.filter(is_cover=True).first() or self.images.first()

    def mark_published(self):
        if not self.published_at:
            self.published_at = timezone.now()

    def increment_views(self):
        Listing.all_objects.filter(pk=self.pk).update(view_count=F("view_count") + 1)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.brand.name}-{self.car_model.name}-{self.title}")[:180]
            slug = base_slug or f"listing-{self.pk or ''}".strip("-")
            counter = 1
            while Listing.all_objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base_slug[:170]}-{counter}"
                counter += 1
            self.slug = slug
        if self.status == ListingStatus.ACTIVE:
            self.mark_published()
        super().save(*args, **kwargs)


class ListingImage(TimeStampedModel):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(
        upload_to=listing_image_upload_to,
        validators=[
            validate_image_file,
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"]),
        ],
    )
    alt_text = models.CharField(max_length=180, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_cover = models.BooleanField(default=False)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = _("Слика од оглас")
        verbose_name_plural = _("Слики од огласи")

    def __str__(self) -> str:
        return f"Слика {self.id} за оглас {self.listing_id}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            if self.is_cover:
                self.listing.images.exclude(pk=self.pk).update(is_cover=False)
            elif not self.listing.images.exclude(pk=self.pk).filter(is_cover=True).exists():
                ListingImage.objects.filter(pk=self.pk).update(is_cover=True)
