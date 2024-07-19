import pandas as pd
import requests_cache
import openmeteo_requests

from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.db.models import Q, Case, When, Value, IntegerField
from django.views.decorators.http import require_GET

from retry_requests import retry

from .utils.cookie import set_last_city_cookie, get_last_city_ids_from_cookie

from .models import City
from .forms import CitySearchForm

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def city_search(request: HttpRequest) -> HttpResponse:
    """Обрабатывает запрос на страницу поиска городов."""

    form = CitySearchForm()
    last_city_ids = get_last_city_ids_from_cookie(request)
    last_cities = City.objects.filter(id__in=last_city_ids).order_by(
        Case(*[When(id=city_id, then=pos) for pos, city_id in enumerate(last_city_ids)])
    )
    context = {'form': form, 'last_cities': last_cities, 'last_city': last_cities.first()}
    return render(request, 'weather/index.html', context=context)


class CityAutocomplete(View):
    """Обрабатывает запросы на автозаполнение городов."""

    def get(self, request, *args, **kwargs):
        term = request.GET.get('term', '')
        cities = City.objects.annotate(
            is_name_match=Q(name__icontains=term),
            is_region_match=Q(region__icontains=term),
            priority=Case(
                When(is_name_match=True, then=Value(1)),
                When(is_region_match=True, then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            )
        ).filter(
            Q(name__icontains=term) | Q(region__icontains=term)
        ).order_by('priority', 'name')[:15]      
        city_list = [{'id': city.id, 'text': city.__str__()} for city in cities]
        return JsonResponse(city_list, safe=False)
    

@require_GET
def get_weather_data(request: HttpRequest) -> HttpResponse:
    """
    Обрабатывает запрос на получение данных о погоде для заданного города.

    Получает данные о текущей и ежедневной погоде из API, обновляет количество запросов для города,
    и сохраняет идентификатор города в cookie.
    """
    
    city_id = request.GET.get('city_id')
    city = get_object_or_404(City, id=city_id)

    city.search_count += 1
    city.save()

    latitude = city.latitude
    longitude = city.longitude

    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current': ['temperature_2m', 'relative_humidity_2m', 'precipitation', 'rain', 'showers', 'snowfall', 'weather_code', 'cloud_cover', 'pressure_msl', 'wind_speed_10m'],
        'daily': ['weather_code', 'temperature_2m_max', 'temperature_2m_min', 'precipitation_sum', 'rain_sum', 'showers_sum', 'snowfall_sum']
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    current = response.Current()
    current_data = {
        'time': current.Time(),
        'temperature_2m': current.Variables(0).Value(),
        'relative_humidity_2m': current.Variables(1).Value(),
        'precipitation': current.Variables(2).Value(),
        'rain': current.Variables(3).Value(),
        'showers': current.Variables(4).Value(),
        'snowfall': current.Variables(5).Value(),
        'weather_code': current.Variables(6).Value(),
        'cloud_cover': current.Variables(7).Value(),
        'pressure_msl': current.Variables(8).Value(),
        'wind_speed_10m': current.Variables(9).Value(),
    }

    daily = response.Daily()
    daily_data = {
        'date': pd.date_range(
            start=pd.to_datetime(daily.Time(), unit='s', utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit='s', utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive='left'
        ).tolist(),
        'weather_code': daily.Variables(0).ValuesAsNumpy().tolist(),
        'temperature_2m_max': daily.Variables(1).ValuesAsNumpy().tolist(),
        'temperature_2m_min': daily.Variables(2).ValuesAsNumpy().tolist(),
        'precipitation_sum': daily.Variables(3).ValuesAsNumpy().tolist(),
        'rain_sum': daily.Variables(4).ValuesAsNumpy().tolist(),
        'showers_sum': daily.Variables(5).ValuesAsNumpy().tolist(),
        'snowfall_sum': daily.Variables(6).ValuesAsNumpy().tolist(),
    }

    weather_data = {
        'city': city.name,
        'city_full_name': city.__str__(),
        'latitude': latitude,
        'longitude': longitude,
        'current': current_data,
        'daily': daily_data,
    }

    json_response = JsonResponse(weather_data)
    set_last_city_cookie(request, json_response, city.id)

    return json_response
