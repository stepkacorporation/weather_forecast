from django.db import models


class City(models.Model):
    """Модель города."""

    name = models.CharField(max_length=255, verbose_name='Город')
    type_of_region = models.CharField(max_length=8, verbose_name='Тип региона')
    region = models.CharField(max_length=255, verbose_name='Регион')
    timezone = models.CharField(max_length=50, verbose_name='Часовой пояс')
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    search_count = models.PositiveBigIntegerField(default=0, verbose_name='Кол-во поисковых запросов')

    def __str__(self) -> str:
        if self.type_of_region == 'Респ':
            return f'{self.name}, {self.type_of_region.lower()}. {self.region}'
        if self.type_of_region == 'край':
            return f'{self.name}, {self.region} {self.type_of_region}'
        if self.type_of_region == 'обл':
            return f'{self.name}, {self.region} {self.type_of_region}.'
        if self.type_of_region == 'г': 
            if self.name == self.region:
                return f'{self.name}'
            return f'{self.region}, {self.name}'
        if self.type_of_region == 'АО':
            if self.region == 'Ханты-Мансийский Автономный округ - Югра':
                return f'{self.name}, {self.region}'
            return f'{self.name}, {self.region} Автономный округ'
        return f'{self.name}, {self.type_of_region}, {self.region}'

    class Meta:
        unique_together = ('name', 'region', 'latitude', 'longitude')
        ordering = ('name',)
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

