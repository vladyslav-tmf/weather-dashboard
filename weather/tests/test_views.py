from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from weather.tests.test_base import WeatherTestBase


class CityViewSetTest(WeatherTestBase, APITestCase):
    """Test cases for CityViewSet."""

    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)

    def test_list_cities(self):
        """Test listing cities."""
        url = reverse("cities-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["name"], "Kyiv")

    def test_with_current_weather(self):
        """Test listing cities with current weather."""
        url = reverse("cities-with-current-weather")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        kyiv_data = next(city for city in response.data if city["name"] == "Kyiv")
        self.assertEqual(kyiv_data["current_weather"]["temperature"], 20.5)

    def test_update_weather_authorized(self):
        """Test updating weather with admin authentication."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("cities-update-weather", kwargs={"pk": self.kyiv.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WeatherDataViewSetTest(WeatherTestBase, APITestCase):
    """Test cases for WeatherDataViewSet."""

    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)

    def test_list_weather_data(self):
        """Test listing weather data."""
        url = reverse("weather-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_by_city(self):
        """Test filtering weather data by city."""
        url = reverse("weather-list")
        response = self.client.get(url, {"city": self.kyiv.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["city"], self.kyiv.pk)

    def test_filter_by_temperature(self):
        """Test filtering weather data by temperature range."""
        url = reverse("weather-list")
        response = self.client.get(url, {"min_temperature": 15, "max_temperature": 18})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["city"], self.london.pk)

    def test_update_all_authorized(self):
        """Test updating all weather data with admin authentication."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("weather-update-all")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
