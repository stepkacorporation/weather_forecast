from django.contrib import admin

from .models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ru', 'country_code', 'latitude', 'longitude', 'search_count')
    search_fields = ('name_en', 'name_ru')
