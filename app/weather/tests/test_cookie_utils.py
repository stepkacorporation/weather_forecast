from django.test import SimpleTestCase, RequestFactory, TestCase
from django.http import HttpResponse
from django.utils import timezone

from datetime import datetime, timedelta

from ..utils.cookie import cookie_date, get_last_city_ids_from_cookie, set_last_city_cookie


class CookieDateTest(SimpleTestCase):
    def test_cookie_date_format(self):
        date = datetime(2024, 7, 19, 12, 0, 0)
        expected_date_str = 'Fri, 19-Jul-2024 12:00:00 GMT'
        self.assertEqual(cookie_date(date), expected_date_str)

    def test_cookie_date_format_with_different_date(self):
        date = datetime(2025, 1, 1, 0, 0, 0)
        expected_date_str = 'Wed, 01-Jan-2025 00:00:00 GMT'
        self.assertEqual(cookie_date(date), expected_date_str)


class GetLastCityIdsFromCookieTest(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_last_city_ids_from_cookie_empty(self):
        request = self.factory.get('/')
        self.assertEqual(get_last_city_ids_from_cookie(request), [])

    def test_get_last_city_ids_from_cookie_with_data(self):
        request = self.factory.get('/')
        request.COOKIES['last_city_ids'] = '1,2,3'
        self.assertEqual(get_last_city_ids_from_cookie(request), [1, 2, 3])

    def test_get_last_city_ids_from_cookie_with_non_digit_data(self):
        request = self.factory.get('/')
        request.COOKIES['last_city_ids'] = '1,a,3'
        self.assertEqual(get_last_city_ids_from_cookie(request), [1, 3])

    def test_get_last_city_ids_from_cookie_with_trailing_comma(self):
        request = self.factory.get('/')
        request.COOKIES['last_city_ids'] = '1,2,3,'
        self.assertEqual(get_last_city_ids_from_cookie(request), [1, 2, 3])


class SetLastCityCookieTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.response = HttpResponse()
        self.city_id = 1

    def test_set_last_city_cookie_empty(self):
        set_last_city_cookie(self.request, self.response, self.city_id)
        self.assertIn('last_city_ids', self.response.cookies)
        self.assertEqual(self.response.cookies['last_city_ids'].value, '1')

    def test_set_last_city_cookie_existing_cookie(self):
        self.request.COOKIES['last_city_ids'] = '2,3'
        set_last_city_cookie(self.request, self.response, self.city_id)
        self.assertEqual(self.response.cookies['last_city_ids'].value, '1,2,3')

    def test_set_last_city_cookie_existing_cookie_with_duplicates(self):
        self.request.COOKIES['last_city_ids'] = '1,2,3'
        set_last_city_cookie(self.request, self.response, self.city_id)
        self.assertEqual(self.response.cookies['last_city_ids'].value, '1,2,3')

    def test_set_last_city_cookie_existing_cookie_with_max_length(self):
        self.request.COOKIES['last_city_ids'] = '2,3,4,5,6,7,8'
        set_last_city_cookie(self.request, self.response, self.city_id)
        self.assertEqual(self.response.cookies['last_city_ids'].value, '1,2,3,4,5,6,7')

    def test_set_last_city_cookie_check_expiry(self):
        set_last_city_cookie(self.request, self.response, self.city_id)
        expected_expiry_date = timezone.now() + timedelta(days=7)
        self.assertEqual(self.response.cookies['last_city_ids']['expires'], cookie_date(expected_expiry_date))

    def test_set_last_city_cookie_existing_cookie_with_non_digit(self):
        self.request.COOKIES['last_city_ids'] = '2,a,3'
        set_last_city_cookie(self.request, self.response, self.city_id)
        self.assertEqual(self.response.cookies['last_city_ids'].value, '1,2,3')
