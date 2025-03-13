from django_filters import rest_framework as filters

from weather.models import WeatherData


class WeatherDataFilter(filters.FilterSet):
    """Filter set for WeatherData model.

    Provides filtering options for weather data:
    - By city ID
    - By city name (case-insensitive partial match)
    - By date range
    - By weather condition
    - By temperature range
    """

    city = filters.NumberFilter(field_name="city_id")
    city_name = filters.CharFilter(field_name="city__name", lookup_expr="icontains")
    date_from = filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    date_to = filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")
    weather_condition = filters.CharFilter(lookup_expr="icontains")
    min_temperature = filters.NumberFilter(field_name="temperature", lookup_expr="gte")
    max_temperature = filters.NumberFilter(field_name="temperature", lookup_expr="lte")

    class Meta:
        model = WeatherData
        fields = [
            "city",
            "city_name",
            "date_from",
            "date_to",
            "weather_condition",
            "min_temperature",
            "max_temperature",
        ]
