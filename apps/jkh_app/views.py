from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import (HouseModel, ApartmentModel, SerialWaterMeterModel, WaterMeterReadings, PaymentRecord)
from .serializers import (HouseSerializer, ApartmentSerializer,
                          SerialWaterMeterSerializer, WaterMeterReadingsSerializer, PaymentRecordSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .tasks import calculate_payments_for_house


class HouseViewSet(viewsets.ModelViewSet):
    queryset = HouseModel.objects.all()
    serializer_class = HouseSerializer


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = ApartmentModel.objects.all()
    serializer_class = ApartmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['house']

    # -----------------------------------------------------------
    # Реализуем возможность выводить данные из нескольких моделей
    # Например в этом эндпоинте мы можем отфильтроваться по дому
    # И увидеть весь список квартир, которые находятся в конкретном доме.
    # И номера счетчиков, которые находятся в квартирах.
    # Например: http://127.0.0.1:8000/api/houses/1/apartments/
    # Мы получаем список квартир которые входят в дом, чей pk=1
    # -----------------------------------------------------------
    def list_apartments_by_house(self, request, house_pk=None):
        house = get_object_or_404(HouseModel, pk=house_pk)
        apartments = ApartmentModel.objects.filter(house=house)
        serializer = ApartmentSerializer(apartments, many=True)
        return Response(serializer.data)


# -----------------------------------------------------------
# оставим в декораторе методы post и get для удобного тестирования
# в браузере, чтобы не заморачиваться через postman или curl,
# так конечно правильней оставить только метод POST
# -----------------------------------------------------------
@api_view(['POST', 'GET'])
def calculate_monthly_payment_view(request, house_id):

    task = calculate_payments_for_house.delay(house_id)

    result = task.get()

    if isinstance(result, dict) and result.get("status") == "error":
        return Response(result, status=400)

    return Response({"status": "success", "payments": result})


class SerialWaterMeterViewSet(viewsets.ModelViewSet):
    queryset = SerialWaterMeterModel.objects.all()
    serializer_class = SerialWaterMeterSerializer


class WaterMeterReadingsViewSet(viewsets.ModelViewSet):
    queryset = WaterMeterReadings.objects.all()
    serializer_class = WaterMeterReadingsSerializer
