import pytest
from django.urls import reverse

from apps.moderation.models import AuditLog, ListingReport
from tests.factories import ListingFactory, UserFactory

pytestmark = pytest.mark.django_db


def test_listing_report_creates_report_and_audit_log(client):
    reporter = UserFactory()
    listing = ListingFactory()
    client.force_login(reporter)

    response = client.post(
        reverse("moderation:report", kwargs={"slug": listing.slug}),
        data={"reason": "fraud", "description": "Opisot deluva sumnitelno."},
        follow=True,
    )

    assert response.status_code == 200
    assert ListingReport.objects.filter(listing=listing, reporter=reporter).exists()
    assert AuditLog.objects.filter(listing=listing, event_type="listing_reported").exists()

