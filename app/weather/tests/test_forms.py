from django import forms
from django.test import SimpleTestCase

from ..forms import CitySearchForm


class CitySearchFormTest(SimpleTestCase):
    def test_form_fields(self):
        form = CitySearchForm()
        self.assertIn('city', form.fields)

    def test_form_field_widget(self):
        form = CitySearchForm()
        self.assertIsInstance(form.fields['city'].widget, forms.Select)
        self.assertEqual(form.fields['city'].widget.attrs['class'], 'city-select form-select')

    def test_form_empty_data(self):
        form = CitySearchForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('city', form.errors)

    def test_form_valid_data(self):
        form = CitySearchForm(data={'city': 'Test City'})
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form = CitySearchForm(data={'city': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('city', form.errors)

    def test_form_data_saved(self):
        data = {'city': 'Test City'}
        form = CitySearchForm(data=data)
        form.is_valid()
        self.assertEqual(form.cleaned_data['city'], data['city'])
