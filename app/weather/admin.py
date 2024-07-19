from django.contrib import admin

from .models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type_of_region', 'region', 'timezone', 'latitude', 'longitude', 'search_count')
    search_fields = ('name', 'type_of_region', 'region')
    list_display_links = ('name', 'region')
