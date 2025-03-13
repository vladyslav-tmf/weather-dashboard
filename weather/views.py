from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from weather.models import City
from weather.serializers import CitySerializer, CityWithCurrentWeatherSerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for cities.
    Provides read-only access to city information with current weather data.
    """

    serializer_class = CitySerializer

    def get_queryset(self) -> QuerySet[City]:
        return City.objects.prefetch_related("weather_data")

    @action(detail=False, methods=["get"])
    def with_current_weather(self, request: Request) -> Response:
        """List all cities with their current weather data."""
        cities = self.get_queryset()
        serializer = CityWithCurrentWeatherSerializer(cities, many=True)
        return Response(serializer.data)
