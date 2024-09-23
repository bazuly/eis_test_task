from django.core.management.base import BaseCommand
from apps.jkh_app.models import (
    HouseModel,
    ApartmentModel,
    WaterMeterModel,
    SerialWaterMeterModel,
    WaterMeterReadings,
    WaterTariffModel,
    AreaTariffModel,
    PaymentRecord,
)
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Populate the database with test data"

    def handle(self, *args, **kwargs):
        house = HouseModel.objects.create(address="ул. Тестовая, 10")

        apartment_1 = ApartmentModel.objects.create(
            house=house, number="1", apartment_area=50.5
        )
        apartment_2 = ApartmentModel.objects.create(
            house=house, number="2", apartment_area=60.0
        )

        water_meter_1 = WaterMeterModel.objects.create(apartment=apartment_1)
        water_meter_2 = WaterMeterModel.objects.create(apartment=apartment_2)
        serial_water_meter_1 = SerialWaterMeterModel.objects.create(
            water_meter=water_meter_1, serial_number="ABC123"
        )
        serial_water_meter_2 = SerialWaterMeterModel.objects.create(
            water_meter=water_meter_2, serial_number="XYZ789"
        )

        WaterMeterReadings.objects.create(
            water_meter=serial_water_meter_1,
            reading_date=timezone.now() - timedelta(days=30),
            water_meter_value=50.5,
        )
        WaterMeterReadings.objects.create(
            water_meter=serial_water_meter_1,
            reading_date=timezone.now(),
            water_meter_value=100.5,
        )

        WaterMeterReadings.objects.create(
            water_meter=serial_water_meter_2,
            reading_date=timezone.now() - timedelta(days=30),
            water_meter_value=55.5,
        )

        WaterMeterReadings.objects.create(
            water_meter=serial_water_meter_2,
            reading_date=timezone.now(),
            water_meter_value=200.0,
        )

        water_tariff = WaterTariffModel.objects.create(cost_per_unit=50.0)
        area_tariff = AreaTariffModel.objects.create(cost_per_unit=10.0)
        PaymentRecord.objects.create(
            apartment=apartment_1,
            date=timezone.now(),
            water_cost=water_tariff,
            area_cost=area_tariff,
            total_area_cost=apartment_1.apartment_area * area_tariff.cost_per_unit,
            total_water_cost=100.5 * water_tariff.cost_per_unit,
            total_cost=(apartment_1.apartment_area * area_tariff.cost_per_unit)
            + (100.5 * water_tariff.cost_per_unit),
        )

        PaymentRecord.objects.create(
            apartment=apartment_2,
            date=timezone.now(),
            water_cost=water_tariff,
            area_cost=area_tariff,
            total_area_cost=apartment_2.apartment_area * area_tariff.cost_per_unit,
            total_water_cost=200.0 * water_tariff.cost_per_unit,
            total_cost=(apartment_2.apartment_area * area_tariff.cost_per_unit)
            + (200.0 * water_tariff.cost_per_unit),
        )

        self.stdout.write(self.style.SUCCESS("Test data added successfully!"))
