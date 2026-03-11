import factory
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.core.models import City
from apps.listings.choices import BodyType, FuelType, ListingCondition, ListingStatus, TransmissionType
from apps.listings.models import CarBrand, CarModel, Listing

User = get_user_model()


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = factory.Sequence(lambda n: f"City {n}")
    region = "Region"
    display_order = factory.Sequence(lambda n: n)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    is_active = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or "DemoPass123!"
        self.set_password(password)
        if create:
            self.save()

    @factory.post_generation
    def profile_data(self, create, extracted, **kwargs):
        if not create:
            return
        self.profile.full_name = f"User {self.pk}"
        self.profile.phone_number = f"+389701010{self.pk:02d}"[:12]
        self.profile.city = CityFactory()
        self.profile.save()


class CarBrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarBrand

    name = factory.Sequence(lambda n: f"Brand {n}")


class CarModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarModel

    brand = factory.SubFactory(CarBrandFactory)
    name = factory.Sequence(lambda n: f"Model {n}")


class ListingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Listing

    seller = factory.SubFactory(UserFactory)
    brand = factory.SubFactory(CarBrandFactory)
    car_model = factory.SubFactory(CarModelFactory, brand=factory.SelfAttribute("..brand"))
    title = factory.Sequence(lambda n: f"Listing {n}")
    description = "Servisiran avtomobil vo dobra sostojba."
    price = 7500
    year = 2017
    mileage = 145000
    fuel_type = FuelType.DIESEL
    transmission = TransmissionType.MANUAL
    body_type = BodyType.SEDAN
    color = "Siva"
    condition = ListingCondition.USED
    city = factory.SubFactory(CityFactory)
    status = ListingStatus.ACTIVE
    show_phone = True
    published_at = factory.LazyFunction(timezone.now)

