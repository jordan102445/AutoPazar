import pytest
from django.urls import reverse

from apps.favorites.models import Favorite
from tests.factories import ListingFactory, UserFactory

pytestmark = pytest.mark.django_db


def test_authenticated_user_can_toggle_favorite(client):
    user = UserFactory()
    listing = ListingFactory()
    client.force_login(user)

    response = client.post(reverse("favorites:toggle", kwargs={"slug": listing.slug}))
    assert response.status_code == 200
    assert Favorite.objects.filter(user=user, listing=listing).exists()

    client.post(reverse("favorites:toggle", kwargs={"slug": listing.slug}))
    assert not Favorite.objects.filter(user=user, listing=listing).exists()

