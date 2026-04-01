import pytest
from django.core.management import call_command

from apps.core.models import City
from apps.core.reference_data import REFERENCE_BRAND_COUNT, REFERENCE_CITY_COUNT
from apps.favorites.models import Favorite
from apps.listings.models import CarBrand, CarModel
from apps.messaging.models import InquiryMessage
from apps.users.models import User

pytestmark = pytest.mark.django_db


def test_sync_reference_data_is_idempotent():
    City.objects.create(name="Stip", slug="stip", region="Istocen", display_order=1)

    call_command("sync_reference_data")

    city_count = City.objects.count()
    brand_count = CarBrand.objects.count()
    model_count = CarModel.objects.count()

    assert city_count == REFERENCE_CITY_COUNT
    assert brand_count >= REFERENCE_BRAND_COUNT
    assert City.objects.filter(name="Скопје", slug="skopje").exists()
    assert City.objects.filter(name="Штип", slug="shtip").exists()
    assert not City.objects.filter(name="Stip").exists()
    assert CarBrand.objects.filter(name="Audi").exists()
    assert CarModel.objects.filter(brand__name="Audi", name="Q5").exists()

    call_command("sync_reference_data")

    assert City.objects.count() == city_count
    assert CarBrand.objects.count() == brand_count
    assert CarModel.objects.count() == model_count


def test_seed_demo_data_is_idempotent():
    call_command("seed_demo_data")

    user_count = User.objects.count()
    city_count = City.objects.count()
    brand_count = CarBrand.objects.count()
    model_count = CarModel.objects.count()
    listing_count = sum(user.listings.count() for user in User.objects.all())
    favorite_count = Favorite.objects.count()
    inquiry_count = InquiryMessage.objects.count()

    call_command("seed_demo_data")

    assert User.objects.count() == user_count
    assert City.objects.count() == city_count
    assert CarBrand.objects.count() == brand_count
    assert CarModel.objects.count() == model_count
    assert sum(user.listings.count() for user in User.objects.all()) == listing_count
    assert Favorite.objects.count() == favorite_count
    assert InquiryMessage.objects.count() == inquiry_count
