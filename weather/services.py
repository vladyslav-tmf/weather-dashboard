import logging

import httpx
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction

from weather.models import City, WeatherData

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for interacting with the OpenWeatherMap API."""

    def __init__(self) -> None:
        self.api_key = settings.OPEN_WEATHER_MAP_API_KEY
        self.api_url = settings.OPEN_WEATHER_MAP_API_URL
        self.units = settings.OPEN_WEATHER_MAP_API_UNITS

        if not self.api_key:
            raise ImproperlyConfigured(
                "OpenWeatherMap API key is not configured. "
                "Please set the OPEN_WEATHER_MAP_API_KEY environment variable."
            )

    def get_temperature_unit(self) -> str:
        """Get temperature unit based on the API units setting."""
        return "°C" if self.units == "metric" else "°F"

    def get_weather_for_city(self, city: City) -> dict:
        """Get current weather data for a city from OpenWeatherMap API."""
        endpoint = f"{self.api_url}weather"
        params = {
            "lat": city.latitude,
            "lon": city.longitude,
            "appid": self.api_key,
            "units": self.units,
        }

        with httpx.Client() as client:
            response = client.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()

    def parse_weather_data(self, city: City, weather_data: dict) -> WeatherData:
        """
        Parse weather data from OpenWeatherMap API response
        and create a WeatherData object.
        """
        main_data = weather_data.get("main", {})

        if not main_data:
            raise ValueError("Missing main weather data")

        wind_data = weather_data.get("wind", {})
        weather_info = weather_data.get("weather", [{}])[0]

        return WeatherData(
            city=city,
            temperature=main_data.get("temp"),
            feels_like=main_data.get("feels_like"),
            humidity=main_data.get("humidity"),
            pressure=main_data.get("pressure"),
            wind_speed=wind_data.get("speed", 0.0),
            wind_direction=wind_data.get("deg", 0),
            weather_condition=weather_info.get("main"),
            weather_description=weather_info.get("description", ""),
            icon=weather_info.get("icon", ""),
        )

    def update_weather_for_city(self, city: City) -> WeatherData | None:
        """Update weather data for a city."""
        try:
            weather_data = self.get_weather_for_city(city)
            weather_obj = self.parse_weather_data(city, weather_data)

            with transaction.atomic():
                weather_obj.save()

            return weather_obj

        except (httpx.HTTPError, ValueError) as error:
            logger.error(f"Failed to update weather for {city.name}: {error}")
            return None

    def update_weather_for_all_cities(self) -> list[WeatherData]:
        """Update weather data for all cities in the database."""
        cities = City.objects.all()
        results = []

        for city in cities:
            weather = self.update_weather_for_city(city)

            if weather:
                results.append(weather)

        return results
