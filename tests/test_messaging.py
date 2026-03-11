import pytest
from django.urls import reverse

from apps.messaging.models import InquiryMessage
from tests.factories import ListingFactory, UserFactory

pytestmark = pytest.mark.django_db


def test_contact_form_creates_inquiry(client):
    listing = ListingFactory()

    response = client.post(
        reverse("messaging:create", kwargs={"slug": listing.slug}),
        data={
            "sender_name": "Interested Buyer",
            "sender_email": "buyer@example.com",
            "sender_phone": "+38970123456",
            "message": "Dali e mozen pregled utre?",
        },
        follow=True,
    )

    assert response.status_code == 200
    assert InquiryMessage.objects.filter(listing=listing, sender_email="buyer@example.com").exists()


def test_user_cannot_message_own_listing(client):
    owner = UserFactory()
    listing = ListingFactory(seller=owner)
    client.force_login(owner)

    response = client.post(
        reverse("messaging:create", kwargs={"slug": listing.slug}),
        data={
            "sender_name": owner.profile.full_name,
            "sender_email": owner.email,
            "sender_phone": owner.profile.phone_number,
            "message": "Self message",
        },
        follow=True,
    )

    assert response.status_code == 200
    assert InquiryMessage.objects.count() == 0

