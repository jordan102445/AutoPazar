from django.core.management.base import BaseCommand

from apps.core.reference_data import (
    REFERENCE_BRAND_COUNT,
    REFERENCE_CITY_COUNT,
    REFERENCE_MODEL_COUNT,
    sync_car_reference_data,
    sync_city_reference_data,
)


class Command(BaseCommand):
    help = "Синхронизирај ги референтните градови и автомобилски марки/модели."

    def handle(self, *args, **options):
        _, created_cities, updated_cities = sync_city_reference_data()
        car_results = sync_car_reference_data()

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Референтните податоци се синхронизирани. "
                    f"Градови: {REFERENCE_CITY_COUNT} "
                    f"(нови: {created_cities}, ажурирани: {updated_cities}). "
                    f"Марки: {REFERENCE_BRAND_COUNT} "
                    f"(нови: {car_results['created_brands']}, ажурирани: {car_results['updated_brands']}). "
                    f"Модели: {REFERENCE_MODEL_COUNT} "
                    f"(нови: {car_results['created_models']}, ажурирани: {car_results['updated_models']})."
                )
            )
        )
