from decimal import Decimal

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
        demo_colors = ["Бела", "Сива", "Црна", "Сина"]
        demo_fuel_types = [FuelType.PETROL, FuelType.DIESEL, FuelType.HYBRID]
        demo_transmissions = [TransmissionType.MANUAL, TransmissionType.AUTOMATIC]
        demo_body_types = [BodyType.SEDAN, BodyType.HATCHBACK, BodyType.SUV]

        users = []
        for idx in range(1, 5):
            email = f"user{idx}@autopazar.mk"
            user, _ = User.objects.get_or_create(email=email, defaults={"is_active": True})
            user.set_password("DemoPass123!")
            user.is_active = True
            user.save(update_fields=["password", "is_active"])
            user.profile.full_name = f"Демо корисник {idx}"
            user.profile.phone_number = f"+3897010000{idx}"
            user.profile.city = cities[(idx - 1) % len(cities)]
            user.profile.bio = "Приватен продавач на одржувани возила."
            user.profile.save()
            users.append(user)

        listings = []
        for idx in range(1, 9):
            selected_model = car_models[idx - 1]
            seller = users[(idx - 1) % len(users)]
            city = cities[(idx + 4) % len(cities)]
            listing, _ = Listing.all_objects.update_or_create(
                seller=seller,
                title=f"{selected_model.brand.name} {selected_model.name} {2013 + idx}",
                defaults={
                    "description": "Редовно сервисиран автомобил, во добра состојба, без скриени трошоци.",
                    "price": Decimal(4500 + idx * 1200),
                    "brand": selected_model.brand,
                    "car_model": selected_model,
                    "year": 2013 + idx,
                    "mileage": 90000 + idx * 17500,
                    "fuel_type": demo_fuel_types[(idx - 1) % len(demo_fuel_types)],
                    "transmission": demo_transmissions[(idx - 1) % len(demo_transmissions)],
                    "body_type": demo_body_types[(idx - 1) % len(demo_body_types)],
                    "color": demo_colors[(idx - 1) % len(demo_colors)],
                    "condition": ListingCondition.USED,
                    "city": city,
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
