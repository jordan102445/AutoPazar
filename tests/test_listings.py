import pytest
from django.urls import reverse

from apps.listings.choices import ListingStatus
from tests.factories import CarBrandFactory, CarModelFactory, CityFactory, ListingFactory, UserFactory

pytestmark = pytest.mark.django_db


def test_listing_owner_can_edit_but_other_user_cannot(client):
    owner = UserFactory()
    stranger = UserFactory()
    listing = ListingFactory(seller=owner)

    client.force_login(owner)
    owner_response = client.get(reverse("listings:update", kwargs={"slug": listing.slug}))
    assert owner_response.status_code == 200

    client.force_login(stranger)
    stranger_response = client.get(reverse("listings:update", kwargs={"slug": listing.slug}))
    assert stranger_response.status_code == 404


def test_listing_filters_apply_brand_city_and_price(client):
    city = CityFactory(name="Bitola")
    other_city = CityFactory(name="Tetovo")
    brand = CarBrandFactory(name="BMW")
    model = CarModelFactory(brand=brand, name="320")
    ListingFactory(brand=brand, car_model=model, city=city, price=9000, title="BMW 320d")
    ListingFactory(city=other_city, price=4500, title="Opel Astra")

    response = client.get(
        reverse("listings:list"),
        {"brand": brand.pk, "city": city.pk, "price_min": 8000, "price_max": 10000},
    )

    listings = list(response.context["listings"])
    assert len(listings) == 1
    assert listings[0].title == "BMW 320d"


def test_listing_status_endpoint_marks_listing_sold(client):
    owner = UserFactory()
    listing = ListingFactory(seller=owner, status=ListingStatus.ACTIVE)
    client.force_login(owner)

    response = client.post(
        reverse("listings:status", kwargs={"slug": listing.slug}),
        data={"action": "mark_sold"},
        follow=True,
    )

    listing.refresh_from_db()
    assert response.status_code == 200
    assert listing.status == ListingStatus.SOLD

