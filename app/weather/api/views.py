from rest_framework import generics

from ..models import City

from .serializers import CitySerializer


class CitySearchCountListView(generics.ListAPIView):
    """API представлеие для получения списка городов с количеством поисковых запросов."""

    queryset = City.objects.all()
    serializer_class = CitySerializer
