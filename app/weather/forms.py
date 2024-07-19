from django import forms


class CitySearchForm(forms.Form):
    """Форма для поиска городов."""
    
    city = forms.CharField(
        label='',
        widget=forms.Select(attrs={'class': 'city-select form-select'})
    )