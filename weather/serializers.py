from rest_framework import serializers

from weather.models import City, WeatherData


class CitySerializer(serializers.ModelSerializer):
    """
    Serializer for the City model.
    Provides serialization of city data including geographical coordinates.
    """

    class Meta:
        model = City
        fields = ["id", "name", "country", "latitude", "longitude", "external_id"]


class WeatherDataSerializer(serializers.ModelSerializer):
    """
    Serializer for the WeatherData model.
    Provides complete weather information with additional city name field.
    """

    city_name = serializers.CharField(source="city.name", read_only=True)

    class Meta:
        model = WeatherData
        fields = [
            "id",
            "city",
            "city_name",
            "temperature",
            "feels_like",
            "humidity",
            "pressure",
            "wind_speed",
            "wind_direction",
            "weather_condition",
            "weather_description",
            "icon",
            "timestamp",
        ]


class CityWithCurrentWeatherSerializer(serializers.ModelSerializer):
    """Serializer for City model with current weather data."""

    current_weather = WeatherDataSerializer()

    class Meta:
        model = City
        fields = ["id", "name", "country", "latitude", "longitude", "current_weather"]
