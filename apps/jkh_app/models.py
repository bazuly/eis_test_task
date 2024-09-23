from django.utils import timezone
from django.db import models


class HouseModel(models.Model):
    address = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return self.address


class ApartmentModel(models.Model):
    house = models.ForeignKey(HouseModel, on_delete=models.CASCADE)
    number = models.CharField(max_length=64, null=False, verbose_name="Номер квартиры")
    apartment_area = models.DecimalField(max_digits=10, decimal_places=2,
                                         verbose_name="Площадь квартиры")

    def __str__(self):
        return f"Квартира {self.number} в доме по адресу {self.house}"


class WaterMeterModel(models.Model):
    """ Модель для хранения счетчиков в квартире """
    apartment = models.ForeignKey(ApartmentModel, on_delete=models.CASCADE, related_name="water_meters")

    def __str__(self):
        return f"Счетчики в квартире {self.apartment}"


class SerialWaterMeterModel(models.Model):
    """ Модель для хранения серийных номеров счетчиков """
    water_meter = models.ForeignKey(WaterMeterModel, on_delete=models.CASCADE, related_name="Счетчик")
    serial_number = models.CharField(max_length=255, null=False, verbose_name="Номер счетчика")

    def __str__(self):
        return f"Счетчик под номером {self.serial_number} для квартиры {self.water_meter.apartment}"


class WaterMeterReadings(models.Model):
    """ Модель для хранения показателей в счетчиках """
    water_meter = models.ForeignKey(SerialWaterMeterModel, on_delete=models.CASCADE,
                                    verbose_name="Серийный номер счетчика")
    reading_date = models.DateField(default=timezone.now)
    water_meter_value = models.DecimalField(max_digits=15, decimal_places=3,
                                            verbose_name="Общий подсчет показателей")

    def __str__(self):
        return (f"Показания счетчика {self.water_meter} за дату"
                f" {self.reading_date} равны {self.water_meter_value}")


class WaterTariffModel(models.Model):
    """ Модель для хранения данных о тарификации воды """

    # ----------------------------------------------------------------------
    # Название тарифа. Например "Тариф на воду".
    # Логика приложения заключается в том, что у нас могут быть разные название тарифов
    # Например на холодную и горячую воду, правильнее на мой взгляд реализовать
    # данную сущность через choices, но в рамках тестового задания оставим один общий тариф
    # ----------------------------------------------------------------------
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2,
                                        verbose_name="Стоимость за кубометр воды")

    def __str__(self):
        return f"Стоимость за кубометр воды {self.cost_per_unit} руб."


class AreaTariffModel(models.Model):
    """ Модель для хранения данных о тарификации площади """
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2,
                                        verbose_name="Стоимость за квадратный метр")


class PaymentRecord(models.Model):
    """ Модель для расчета коммунальных услуг """
    apartment = models.ForeignKey(ApartmentModel, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Дата расчета")
    water_consumption = models.DecimalField(max_digits=15, decimal_places=3,
                                            verbose_name="Общий расход воды", blank=True, null=True),
    water_cost = models.ForeignKey(WaterTariffModel, on_delete=models.CASCADE)
    area_cost = models.ForeignKey(AreaTariffModel, on_delete=models.CASCADE)
    total_area_cost = models.DecimalField(max_digits=10, decimal_places=2,
                                                    verbose_name="Стоимость за содержание общего имущества")
    total_water_cost = models.DecimalField(max_digits=10, decimal_places=2,
                                            verbose_name="Полная стоимость")
    total_cost = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"Оплата для квартиры {self.apartment}"

