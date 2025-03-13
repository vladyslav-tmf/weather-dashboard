from weather.serializers import CitySerializer, WeatherDataSerializer
from weather.tests.test_base import WeatherTestBase


class CitySerializerTest(WeatherTestBase):
    """Test cases for CitySerializer."""

    def test_city_serializer(self):
        """Test CitySerializer output."""
        serializer = CitySerializer(self.kyiv)
        expected_data = {
            "id": self.kyiv.id,
            "name": "Kyiv",
            "country": "Ukraine",
            "latitude": 50.4501,
            "longitude": 30.5234,
            "external_id": None,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_city_serializer_validation(self):
        """Test CitySerializer validation."""
        invalid_data = {
            "name": "Test City",
            "country": "Test Country",
            "latitude": 200,
            "longitude": 30.5234,
        }
        serializer = CitySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("latitude", serializer.errors)


class WeatherDataSerializerTest(WeatherTestBase):
    """Test cases for WeatherDataSerializer."""

    def test_weather_data_serializer(self):
        """Test WeatherDataSerializer output."""
        serializer = WeatherDataSerializer(self.kyiv_weather)
        expected_data = {
            "id": self.kyiv_weather.id,
            "city": self.kyiv.id,
            "city_name": "Kyiv",
            "temperature": 20.5,
            "feels_like": 19.8,
            "humidity": 65,
            "pressure": 1015,
            "wind_speed": 3.5,
            "wind_direction": 180,
            "weather_condition": "Clear",
            "weather_description": "clear sky",
            "icon": "01d",
            "timestamp": self.kyiv_weather.timestamp.isoformat().replace("+00:00", "Z"),
        }
        self.assertEqual(serializer.data, expected_data)

    def test_weather_data_serializer_validation(self):
        """Test WeatherDataSerializer validation."""
        invalid_data = {
            "city": self.kyiv.id,
            "temperature": "not a number",
            "feels_like": 19.8,
            "humidity": 65,
            "pressure": 1015,
            "wind_speed": 3.5,
            "wind_direction": 180,
            "weather_condition": "Clear",
            "weather_description": "clear sky",
            "icon": "01d",
        }
        serializer = WeatherDataSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("temperature", serializer.errors)
