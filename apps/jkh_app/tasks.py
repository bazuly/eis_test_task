from decimal import Decimal
from apps.jkh_app.models import (
    ApartmentModel, SerialWaterMeterModel, WaterMeterReadings,
    WaterTariffModel, AreaTariffModel, PaymentRecord, HouseModel
)
from celery import shared_task

from apps.jkh_app.serializers import PaymentRecordSerializer


@shared_task
def calculate_payments_for_house(house_id):
    house = HouseModel.objects.get(pk=house_id)
    apartments = ApartmentModel.objects.filter(house=house)
    payment_records = []
    # -----------------------------------------------------------
    # Так как в рамках ТЗ у нас нет задачи привязывать
    # различные тарифы к квартире или воде, поэтому используем
    # две константы. Тариф на воду и тариф на кв. Метр в квартире.
    # В полноценном проекте это были бы две отдельные модели, связанные с
    # Другими моделями OneToMany.
    # Например, модель тарифов на квартиру зависела бы от типа дома, локации,
    # кол-ва комнат, льгот пользователя и т.д.
    # -----------------------------------------------------------
    water_tariff = WaterTariffModel.objects.first()
    area_tariff = AreaTariffModel.objects.first()

    if not water_tariff or not area_tariff:
        return {"status": "error", "message": "Тарифы не найдены"}

    for apartment in apartments:
        serial_water_meters = SerialWaterMeterModel.objects.filter(
            water_meter__apartment=apartment
        )

        if not serial_water_meters.exists():
            continue

        total_water_cost = Decimal(0)
        total_area_cost = Decimal(0)

        for serial_meter in serial_water_meters:
            readings = WaterMeterReadings.objects.filter(water_meter=serial_meter).order_by('-reading_date')[:2]

            if len(readings) < 2:
                continue

            current_reading = readings[0]
            previous_reading = readings[1]

            water_consumption = current_reading.water_meter_value - previous_reading.water_meter_value
            if water_consumption < 0:
                continue

            water_cost = water_consumption * water_tariff.cost_per_unit
            total_water_cost += water_cost

        area_cost = apartment.apartment_area * area_tariff.cost_per_unit
        total_area_cost += area_cost

        total_cost = total_water_cost + total_area_cost

        payment_record = PaymentRecord.objects.create(
            apartment=apartment,
            date=current_reading.reading_date,
            water_cost=water_tariff,
            area_cost=area_tariff,
            total_area_cost=total_area_cost,
            total_water_cost=total_water_cost,
            total_cost=total_cost
        )

        payment_records.append(payment_record)

    serialized_records = PaymentRecordSerializer(payment_records, many=True).data
    return serialized_records
