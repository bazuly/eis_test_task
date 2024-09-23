from rest_framework import serializers
from .models import (HouseModel, ApartmentModel,
                     SerialWaterMeterModel, WaterMeterReadings,
                     WaterTariffModel, AreaTariffModel, WaterMeterModel, PaymentRecord)


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseModel
        fields = '__all__'


class SerialWaterMeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerialWaterMeterModel
        fields = ['id', 'serial_number']


class WaterMeterSerializer(serializers.ModelSerializer):
    serial_numbers = SerialWaterMeterSerializer(many=True, read_only=True, source="Счетчик")

    class Meta:
        model = WaterMeterModel
        fields = ['id', 'serial_numbers']


class ApartmentSerializer(serializers.ModelSerializer):
    house = HouseSerializer(read_only=True)
    water_meters = WaterMeterSerializer(many=True, read_only=True)

    class Meta:
        model = ApartmentModel
        fields = ['id', 'number', 'apartment_area', 'house', 'water_meters']


class WaterMeterReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterMeterReadings
        fields = '__all__'


class WaterTariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterTariffModel
        fields = '__all__'


class AreaTariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaTariffModel
        fields = '__all__'


class PaymentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRecord
        fields = "__all__"
