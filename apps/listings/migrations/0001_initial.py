import decimal
import apps.core.validators
import apps.listings.models
import django.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CarBrand",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=120, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=140, unique=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Car brand",
                "verbose_name_plural": "Car brands",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="CarModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=120)),
                ("slug", models.SlugField(blank=True, max_length=140)),
                ("is_active", models.BooleanField(default=True)),
                ("brand", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="models", to="listings.carbrand")),
            ],
            options={
                "verbose_name": "Car model",
                "verbose_name_plural": "Car models",
                "ordering": ["brand__name", "name"],
                "unique_together": {("brand", "name")},
            },
        ),
        migrations.CreateModel(
            name="Listing",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("title", models.CharField(max_length=180)),
                ("slug", models.SlugField(blank=True, max_length=220, unique=True)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("currency", models.CharField(choices=[("EUR", "EUR"), ("MKD", "MKD")], default="EUR", max_length=3)),
                ("negotiable", models.BooleanField(default=False)),
                ("trim", models.CharField(blank=True, max_length=120)),
                (
                    "year",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1950),
                            django.core.validators.MaxValueValidator(2027),
                        ]
                    ),
                ),
                ("mileage", models.PositiveIntegerField()),
                (
                    "fuel_type",
                    models.CharField(
                        choices=[
                            ("petrol", "Petrol"),
                            ("diesel", "Diesel"),
                            ("lpg", "LPG"),
                            ("cng", "CNG"),
                            ("hybrid", "Hybrid"),
                            ("electric", "Electric"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "transmission",
                    models.CharField(
                        choices=[
                            ("manual", "Manual"),
                            ("automatic", "Automatic"),
                            ("semi_automatic", "Semi-automatic"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "body_type",
                    models.CharField(
                        choices=[
                            ("sedan", "Sedan"),
                            ("hatchback", "Hatchback"),
                            ("coupe", "Coupe"),
                            ("cabrio", "Cabrio"),
                            ("wagon", "Wagon"),
                            ("suv", "SUV"),
                            ("pickup", "Pickup"),
                            ("van", "Van"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "engine_size",
                    models.DecimalField(
                        blank=True,
                        decimal_places=1,
                        max_digits=3,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(decimal.Decimal("0.6")),
                            django.core.validators.MaxValueValidator(decimal.Decimal("9.0")),
                        ],
                    ),
                ),
                ("horsepower", models.PositiveSmallIntegerField(blank=True, null=True)),
                (
                    "drive_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("fwd", "Front wheel drive"),
                            ("rwd", "Rear wheel drive"),
                            ("awd", "All wheel drive"),
                            ("4x4", "4x4"),
                        ],
                        max_length=20,
                    ),
                ),
                ("color", models.CharField(max_length=60)),
                (
                    "condition",
                    models.CharField(
                        choices=[("used", "Used"), ("new", "New"), ("damaged", "Damaged")],
                        max_length=20,
                    ),
                ),
                ("registered_until", models.DateField(blank=True, null=True)),
                ("first_owner", models.BooleanField(blank=True, null=True)),
                ("service_history", models.BooleanField(blank=True, null=True)),
                ("imported", models.BooleanField(blank=True, null=True)),
                ("number_of_doors", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("vin", models.CharField(blank=True, max_length=17)),
                ("show_vin", models.BooleanField(default=False)),
                ("show_phone", models.BooleanField(default=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("pending_moderation", "Pending moderation"),
                            ("active", "Active"),
                            ("sold", "Sold"),
                            ("archived", "Archived"),
                        ],
                        default="draft",
                        max_length=20,
                    ),
                ),
                ("featured", models.BooleanField(default=False)),
                ("published_at", models.DateTimeField(blank=True, null=True)),
                ("view_count", models.PositiveIntegerField(default=0)),
                ("brand", models.ForeignKey(on_delete=models.deletion.PROTECT, related_name="listings", to="listings.carbrand")),
                ("car_model", models.ForeignKey(on_delete=models.deletion.PROTECT, related_name="listings", to="listings.carmodel")),
                ("city", models.ForeignKey(on_delete=models.deletion.PROTECT, related_name="listings", to="core.city")),
                ("seller", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="listings", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Listing",
                "verbose_name_plural": "Listings",
                "ordering": ["-featured", "-published_at", "-created_at"],
                "indexes": [
                    models.Index(fields=["status", "created_at"], name="listings_li_status_79eb7c_idx"),
                    models.Index(fields=["brand", "car_model"], name="listings_li_brand_i_95d9da_idx"),
                    models.Index(fields=["city", "year"], name="listings_li_city_id_01d217_idx"),
                    models.Index(fields=["price", "created_at"], name="listings_li_price_2d0d67_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="ListingImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "image",
                    models.ImageField(
                        upload_to=apps.listings.models.listing_image_upload_to,
                        validators=[
                            apps.core.validators.validate_image_file,
                            django.core.validators.FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"]),
                        ],
                    ),
                ),
                ("alt_text", models.CharField(blank=True, max_length=180)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                ("is_cover", models.BooleanField(default=False)),
                ("listing", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="images", to="listings.listing")),
            ],
            options={
                "verbose_name": "Listing image",
                "verbose_name_plural": "Listing images",
                "ordering": ["sort_order", "id"],
            },
        ),
    ]
