from decimal import Decimal
from random import choice, randint

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.core.reference_data import sync_car_reference_data, sync_city_reference_data
from apps.favorites.models import Favorite
from apps.listings.choices import BodyType, FuelType, ListingCondition, ListingStatus, TransmissionType
from apps.listings.models import Listing
from apps.messaging.models import InquiryMessage

User = get_user_model()


class Command(BaseCommand):
    help = "Внеси демо градови, марки, корисници, огласи, омилени и пораки."

    def handle(self, *args, **options):
        cities, _, _ = sync_city_reference_data()
        car_results = sync_car_reference_data()
        car_models = car_results["models"]

        users = []
        for idx in range(1, 5):
            email = f"user{idx}@autopazar.mk"
            user, created = User.objects.get_or_create(email=email, defaults={"is_active": True})
            if created:
                user.set_password("DemoPass123!")
                user.save()
            user.profile.full_name = f"Демо корисник {idx}"
            user.profile.phone_number = f"+3897010000{idx}"
            user.profile.city = cities[(idx - 1) % len(cities)]
            user.profile.bio = "Приватен продавач на одржувани возила."
            user.profile.save()
            users.append(user)

        listings = []
        for idx in range(1, 9):
            selected_model = choice(car_models)
            listing, _ = Listing.all_objects.get_or_create(
                seller=choice(users),
                title=f"{selected_model.brand.name} {selected_model.name} {2013 + idx}",
                defaults={
                    "description": "Редовно сервисиран автомобил, во добра состојба, без скриени трошоци.",
                    "price": Decimal(4500 + idx * 1200),
                    "brand": selected_model.brand,
                    "car_model": selected_model,
                    "year": 2013 + idx,
                    "mileage": randint(90000, 240000),
                    "fuel_type": choice([FuelType.PETROL, FuelType.DIESEL, FuelType.HYBRID]),
                    "transmission": choice([TransmissionType.MANUAL, TransmissionType.AUTOMATIC]),
                    "body_type": choice([BodyType.SEDAN, BodyType.HATCHBACK, BodyType.SUV]),
                    "color": choice(["Бела", "Сива", "Црна", "Сина"]),
                    "condition": ListingCondition.USED,
                    "city": choice(cities),
                    "status": ListingStatus.ACTIVE,
                    "negotiable": True,
                    "show_phone": True,
                },
            )
            listings.append(listing)

        for user in users:
            for listing in listings[:2]:
                if listing.seller != user:
                    Favorite.objects.get_or_create(user=user, listing=listing)

        if listings:
            InquiryMessage.objects.get_or_create(
                listing=listings[0],
                seller=listings[0].seller,
                sender=users[-1],
                sender_name=users[-1].profile.full_name,
                sender_email=users[-1].email,
                sender_phone=users[-1].profile.phone_number,
                defaults={"message": "Здраво, дали автомобилот е сè уште достапен?"},
            )

        self.stdout.write(self.style.SUCCESS("Демо податоците се успешно внесени."))
