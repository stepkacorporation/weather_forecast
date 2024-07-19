from django.test import TestCase

from ..models import City


class CityModelTest(TestCase):
    def setUp(self):
        self.city1 = City.objects.create(
            name='Москва',
            type_of_region='г',
            region='Москва',
            timezone='UTC+3',
            latitude=55.7558,
            longitude=37.6176,
            search_count=10
        )
        self.city2 = City.objects.create(
            name='Санкт-Петербург',
            type_of_region='г',
            region='Санкт-Петербург',
            timezone='UTC+3',
            latitude=59.9343,
            longitude=30.3351,
            search_count=5
        )

    def test_city_str_method(self):
        city3 = City.objects.create(
            name='Казань',
            type_of_region='Респ',
            region='Татарстан',
            timezone='UTC+3',
            latitude=55.7963,
            longitude=49.1088
        )
        self.assertEqual(str(self.city1), 'Москва')
        self.assertEqual(str(self.city2), 'Санкт-Петербург')
        self.assertEqual(str(city3), 'Казань, респ. Татарстан')

    def test_city_unique_together(self):
        with self.assertRaises(Exception):
            City.objects.create(
                name='Москва',
                type_of_region='г',
                region='Москва',
                timezone='UTC+3',
                latitude=55.7558,
                longitude=37.6176
            )

    def test_city_ordering(self):
        cities = City.objects.all()
        self.assertEqual(cities[0], self.city1)
        self.assertEqual(cities[1], self.city2)

    def test_city_search_count_default(self):
        city4 = City.objects.create(
            name='Новосибирск',
            type_of_region='обл',
            region='Новосибирская область',
            timezone='UTC+7',
            latitude=55.0084,
            longitude=82.9357
        )
        self.assertEqual(city4.search_count, 0)

    def test_city_timezone_field(self):
        self.assertEqual(self.city1.timezone, 'UTC+3')
        self.assertEqual(self.city2.timezone, 'UTC+3')

    def test_city_latitude_longitude_fields(self):
        self.assertEqual(self.city1.latitude, 55.7558)
        self.assertEqual(self.city1.longitude, 37.6176)
        self.assertEqual(self.city2.latitude, 59.9343)
        self.assertEqual(self.city2.longitude, 30.3351)

    def test_city_type_of_region(self):
        city5 = City.objects.create(
            name='Краснодар',
            type_of_region='край',
            region='Краснодарский',
            timezone='UTC+3',
            latitude=45.0355,
            longitude=38.9753
        )
        self.assertEqual(city5.type_of_region, 'край')
        self.assertEqual(str(city5), 'Краснодар, Краснодарский край')

    def test_city_region(self):
        self.assertEqual(self.city1.region, 'Москва')
        self.assertEqual(self.city2.region, 'Санкт-Петербург')

    def test_city_search_count_increment(self):
        initial_count = self.city1.search_count
        self.city1.search_count += 1
        self.city1.save()
        self.city1.refresh_from_db()
        self.assertEqual(self.city1.search_count, initial_count + 1)

    def test_city_verbose_names(self):
        self.assertEqual(City._meta.verbose_name, 'Город')
        self.assertEqual(City._meta.verbose_name_plural, 'Города')

