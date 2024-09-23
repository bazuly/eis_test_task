from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    HouseViewSet, ApartmentViewSet, SerialWaterMeterViewSet,
    WaterMeterReadingsViewSet, calculate_monthly_payment_view
)

router = DefaultRouter()
router.register(r'houses', HouseViewSet)
router.register(r'apartments', ApartmentViewSet)
router.register(r'water_meters', SerialWaterMeterViewSet)
router.register(r'water_meter_readings', WaterMeterReadingsViewSet)

# Регистрация дополнительных маршрутов
urlpatterns = [
    path('houses/<int:house_pk>/apartments/', ApartmentViewSet.as_view({'get': 'list_apartments_by_house'})),
    path('calculate-payment/<int:house_id>/', calculate_monthly_payment_view, name='calculate-payment'),
]

urlpatterns += router.urls
