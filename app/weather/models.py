from django.db import models


class City(models.Model):
    """Модель города."""

    name_en = models.CharField(max_length=255, verbose_name='Название (en)')
    name_ru = models.CharField(max_length=255, verbose_name='Название (ru)', blank=True, null=True)
    country_code = models.CharField(max_length=255, verbose_name='Код страны')
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    search_count = models.PositiveBigIntegerField(default=0, verbose_name='Кол-во поисковых запросов')

    def __str__(self) -> str:
        if self.name_ru:
            return f'{self.name_en} ({self.name_ru}), {self.country_code}'
        return f'{self.name_en}, {self.country_code}'
    
    class Meta:
        unique_together = ('name_en', 'country_code', 'latitude', 'longitude')
        ordering = ('name_en', 'name_ru', 'country_code')
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

