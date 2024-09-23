from django.contrib import admin
from .models import *

admin.site.register(HouseModel)
admin.site.register(SerialWaterMeterModel)
admin.site.register(WaterMeterReadings)
admin.site.register(ApartmentModel)
admin.site.register(WaterTariffModel)
admin.site.register(AreaTariffModel)
admin.site.register(PaymentRecord)
admin.site.register(WaterMeterModel)

