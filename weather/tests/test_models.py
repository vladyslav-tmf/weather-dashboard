from django.core.exceptions import ValidationError
from django.test import override_settings
from django.utils import timezone

from weather.models import City, WeatherData
from weather.tests.test_base import WeatherTestBase


class CityModelTest(WeatherTestBase):
    """Test cases for City model."""

    def test_city_str(self):
        """Test City string representation."""
        self.assertEqual(str(self.kyiv), "Kyiv, Ukraine")
        self.assertEqual(str(self.london), "London, United Kingdom")

    def test_city_current_weather(self):
        """Test City current_weather property."""
        self.assertEqual(self.kyiv.current_weather, self.kyiv_weather)

        self.kyiv_weather.delete()
        self.assertIsNone(self.kyiv.current_weather)

    def test_city_latitude_validation(self):
        """Test City latitude validation."""
        with self.assertRaises(ValidationError):
            city = City(
                name="Invalid City",
                country="Test Country",
                latitude=91,
                longitude=0,
            )
            city.full_clean()

        with self.assertRaises(ValidationError):
            city = City(
                name="Invalid City",
                country="Test Country",
                latitude=-91,
                longitude=0,
            )
            city.full_clean()

    def test_city_longitude_validation(self):
        """Test City longitude validation."""
        with self.assertRaises(ValidationError):
            city = City(
                name="Invalid City",
                country="Test Country",
                latitude=0,
                longitude=181,
            )
            city.full_clean()

        with self.assertRaises(ValidationError):
            city = City(
                name="Invalid City",
                country="Test Country",
                latitude=0,
                longitude=-181,
            )
            city.full_clean()


class WeatherDataModelTest(WeatherTestBase):
    """Test cases for WeatherData model."""

    def test_weather_data_str_metric(self):
        """Test WeatherData string representation in metric units."""
        with override_settings(OPEN_WEATHER_MAP_API_UNITS="metric"):
            expected = (
                f"{self.kyiv.name}: {self.kyiv_weather.temperature}°C at "
                f"{self.kyiv_weather.timestamp}"
            )
            self.assertEqual(str(self.kyiv_weather), expected)

    def test_weather_data_str_imperial(self):
        """Test WeatherData string representation in imperial units."""
        with override_settings(OPEN_WEATHER_MAP_API_UNITS="imperial"):
            expected = (
                f"{self.kyiv.name}: {self.kyiv_weather.temperature}°F at "
                f"{self.kyiv_weather.timestamp}"
            )
            self.assertEqual(str(self.kyiv_weather), expected)

    def test_weather_data_ordering(self):
        """Test WeatherData ordering by timestamp."""
        weather_data = WeatherData.objects.filter(city=self.kyiv)
        self.assertEqual(list(weather_data), [self.kyiv_weather])

        older_weather = WeatherData.objects.create(
            city=self.kyiv,
            temperature=19.5,
            feels_like=18.8,
            humidity=60,
            pressure=1012,
            wind_speed=2.5,
            wind_direction=90,
            weather_condition="Clear",
            weather_description="clear sky",
            icon="01d",
        )
        older_weather.timestamp = self.kyiv_weather.timestamp - timezone.timedelta(
            hours=1
        )
        older_weather.save()

        weather_data = WeatherData.objects.filter(city=self.kyiv)
        self.assertEqual(list(weather_data), [self.kyiv_weather, older_weather])

    def test_weather_data_validation(self):
        """Test WeatherData field validation."""
        with self.assertRaises(ValidationError):
            weather = WeatherData(
                city=self.kyiv,
                temperature=20.5,
                feels_like=19.8,
                humidity=101,
                pressure=1015,
                wind_speed=3.5,
                wind_direction=180,
                weather_condition="Clear",
                weather_description="clear sky",
                icon="01d",
            )
            weather.full_clean()

        with self.assertRaises(ValidationError):
            weather = WeatherData(
                city=self.kyiv,
                temperature=20.5,
                feels_like=19.8,
                humidity=65,
                pressure=1300,
                wind_speed=3.5,
                wind_direction=180,
                weather_condition="Clear",
                weather_description="clear sky",
                icon="01d",
            )
            weather.full_clean()

        with self.assertRaises(ValidationError):
            weather = WeatherData(
                city=self.kyiv,
                temperature=20.5,
                feels_like=19.8,
                humidity=65,
                pressure=1015,
                wind_speed=-1,
                wind_direction=180,
                weather_condition="Clear",
                weather_description="clear sky",
                icon="01d",
            )
            weather.full_clean()

        with self.assertRaises(ValidationError):
            weather = WeatherData(
                city=self.kyiv,
                temperature=20.5,
                feels_like=19.8,
                humidity=65,
                pressure=1015,
                wind_speed=3.5,
                wind_direction=361,
                weather_condition="Clear",
                weather_description="clear sky",
                icon="01d",
            )
            weather.full_clean()
