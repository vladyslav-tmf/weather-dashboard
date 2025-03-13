from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from weather.models import City, WeatherData

User = get_user_model()


class WeatherTestBase(TestCase):
    """Base test class for weather app."""

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.admin_user = User.objects.create_superuser(
            username="admin", password="admin123"
        )

        self.kyiv = City.objects.create(
            name="Kyiv", country="Ukraine", latitude=50.4501, longitude=30.5234
        )
        self.london = City.objects.create(
            name="London", country="United Kingdom", latitude=51.5074, longitude=-0.1278
        )

        self.kyiv_weather = WeatherData.objects.create(
            city=self.kyiv,
            temperature=20.5,
            feels_like=19.8,
            humidity=65,
            pressure=1015,
            wind_speed=3.5,
            wind_direction=180,
            weather_condition="Clear",
            weather_description="clear sky",
            icon="01d",
        )
        self.london_weather = WeatherData.objects.create(
            city=self.london,
            temperature=15.5,
            feels_like=14.8,
            humidity=75,
            pressure=1010,
            wind_speed=4.5,
            wind_direction=270,
            weather_condition="Clouds",
            weather_description="scattered clouds",
            icon="03d",
        )
