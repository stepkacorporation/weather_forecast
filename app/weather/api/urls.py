from django.urls import path
from .views import CitySearchCountListView

urlpatterns = [
    path('cities/search-count/', CitySearchCountListView.as_view(), name='city-search-count-list'),
]
