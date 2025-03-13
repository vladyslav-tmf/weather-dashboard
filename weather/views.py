from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from weather.models import City, WeatherData
from weather.serializers import CitySerializer, CityWithCurrentWeatherSerializer, \
    WeatherDataSerializer


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


class WeatherDataViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for weather data.
    Provides read-only access to weather information with filtering.
    """

    serializer_class = WeatherDataSerializer

    def get_queryset(self) -> QuerySet[WeatherData]:
        queryset = WeatherData.objects.select_related("city")

        city_id = self.request.query_params.get("city")
        date_from = self.request.query_params.get("from")
        date_to = self.request.query_params.get("to")

        if city_id:
            queryset = queryset.filter(city_id=city_id)

        if date_from:
            queryset = queryset.filter(timestamp__gte=date_from)

        if date_to:
            queryset = queryset.filter(timestamp__lte=date_to)

        return queryset
