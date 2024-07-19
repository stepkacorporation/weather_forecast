from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import City


class CitySearchCountListViewTests(APITestCase):
    def setUp(self):
        self.city1 = City.objects.create(
            name='Москва',
            type_of_region='г',
            region='Центральный',
            timezone='UTC+3',
            latitude=55.7558,
            longitude=37.6173,
            search_count=10
        )
        self.city2 = City.objects.create(
            name='Санкт-Петербург',
            type_of_region='г',
            region='Северо-Западный',
            timezone='UTC+3',
            latitude=59.9343,
            longitude=30.3351,
            search_count=5
        )
        self.url = reverse('city-search-count-list')

    def test_get_city_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_city_serializer(self):
        response = self.client.get(self.url)
        data = response.json()['results']
        self.assertTrue(any(city['name'] == self.city1.name for city in data))
        self.assertTrue(any(city['search_count'] == self.city1.search_count for city in data))
        self.assertTrue(any(city['name'] == self.city2.name for city in data))
        self.assertTrue(any(city['search_count'] == self.city2.search_count for city in data))
