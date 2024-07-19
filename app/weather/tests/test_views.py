import json

from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.http import JsonResponse

from ..models import City
from ..views import CityAutocomplete


class CitySearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.city1 = City.objects.create(
            name='Москва',
            type_of_region='г',
            region='Москва',
            timezone='Europe/Moscow',
            latitude=55.7558,
            longitude=37.6176
        )

    def test_city_search_view(self):
        response = self.client.get(reverse('city-search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/index.html')

    def test_city_search_view_with_last_cities(self):
        self.client.cookies['last_city_ids'] = str(self.city1.id)
        response = self.client.get(reverse('city-search'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('last_cities', response.context)
        self.assertEqual(response.context['last_cities'].first(), self.city1)


class CityAutocompleteViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.city1 = City.objects.create(
            name='Москва',
            type_of_region='г',
            region='Москва',
            timezone='Europe/Moscow',
            latitude=55.7558,
            longitude=37.6176
        )
        self.city2 = City.objects.create(
            name='Санкт-Петербург',
            type_of_region='г',
            region='Санкт-Петербург',
            timezone='Europe/Moscow',
            latitude=59.9343,
            longitude=30.3351
        )

    def test_city_autocomplete_view(self):
        request = self.factory.get(reverse('city-autocomplete'), {'term': 'Москва'})
        response = CityAutocomplete.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        city_list = json.loads(response.content)
        self.assertEqual(len(city_list), 1)
        self.assertEqual(city_list[0]['text'], str(self.city1))
