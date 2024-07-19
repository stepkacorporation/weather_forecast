from django.urls import path

from .views import city_search, CityAutocomplete, get_weather_data

urlpatterns = [
    path('', city_search, name='city-search'),
    path('city-autocomplete/', CityAutocomplete.as_view(), name='city-autocomplete'),
    path('get-weather-data/', get_weather_data, name='get-weather-data'),
]
