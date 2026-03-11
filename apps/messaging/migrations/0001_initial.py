from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("listings", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="InquiryMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("sender_name", models.CharField(max_length=180)),
                ("sender_email", models.EmailField(max_length=254)),
                ("sender_phone", models.CharField(blank=True, max_length=32)),
                ("message", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[("new", "New"), ("replied", "Replied"), ("archived", "Archived")],
                        default="new",
                        max_length=20,
                    ),
                ),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("user_agent", models.CharField(blank=True, max_length=255)),
                ("is_spam", models.BooleanField(default=False)),
                ("listing", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="inquiries", to="listings.listing")),
                ("seller", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="received_inquiries", to=settings.AUTH_USER_MODEL)),
                (
                    "sender",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=models.deletion.SET_NULL,
                        related_name="sent_inquiries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Inquiry",
                "verbose_name_plural": "Inquiries",
                "ordering": ["-created_at"],
            },
        ),
    ]

