from django.db.models import QuerySet
from django.views.generic import TemplateView
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from weather.filters import WeatherDataFilter
from weather.models import City, WeatherData
from weather.serializers import (
    CitySerializer,
    CityWithCurrentWeatherSerializer,
    WeatherDataSerializer,
)
from weather.services import WeatherService


class DashboardView(TemplateView):
    template_name = "weather/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cities"] = City.objects.prefetch_related("weather_data")
        return context


@extend_schema_view(
    list=extend_schema(
        summary="List cities",
        description="Get a list of all cities with pagination.",
    ),
    retrieve=extend_schema(
        summary="Get city details",
        description="Get detailed information about a specific city.",
    ),
    with_current_weather=extend_schema(
        summary="List cities with current weather",
        description="Get a list of all cities with their current weather data.",
        responses={status.HTTP_200_OK: CityWithCurrentWeatherSerializer(many=True)},
    ),
    update_weather=extend_schema(
        summary="Update city weather",
        description=(
            "Update weather data for a specific city. Requires admin privileges."
        ),
        responses={status.HTTP_200_OK: WeatherDataSerializer},
    ),
)
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

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def update_weather(self, request: Request, pk: int = None):
        """Update weather data for a specific city."""
        city = self.get_object()

        weather_service = WeatherService()
        weather_data = weather_service.update_weather_for_city(city)

        if weather_data:
            serializer = WeatherDataSerializer(weather_data)
            return Response(serializer.data)

        return Response(
            {"error": "Failed to update weather data"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@extend_schema_view(
    list=extend_schema(
        summary="List weather data",
        description=(
            "Get a list of all weather data entries "
            "with pagination and filtering options."
        ),
    ),
    retrieve=extend_schema(
        summary="Get weather data details",
        description="Get detailed information about specific weather data entry.",
    ),
    update_all=extend_schema(
        summary="Update all cities weather",
        description="Update weather data for all cities. Requires admin privileges.",
        responses={status.HTTP_200_OK: WeatherDataSerializer(many=True)},
    ),
)
class WeatherDataViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for weather data.
    Provides read-only access to weather information with filtering.
    """

    queryset = WeatherData.objects.select_related("city")
    serializer_class = WeatherDataSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = WeatherDataFilter

    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def update_all(self, request: Request) -> Response:
        """Update weather data for all cities."""
        weather_service = WeatherService()
        results = weather_service.update_weather_for_all_cities()

        if results:
            serializer = WeatherDataSerializer(results, many=True)
            return Response(serializer.data)

        return Response(
            {"error": "Failed to update weather data for any city"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
