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

    def validate_latitude(self, value):
        """Validate latitude is between -90 and 90 degrees."""
        if not -90 <= value <= 90:
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90 degrees."
            )
        return value

    def validate_longitude(self, value):
        """Validate longitude is between -180 and 180 degrees."""
        if not -180 <= value <= 180:
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180 degrees."
            )
        return value


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
