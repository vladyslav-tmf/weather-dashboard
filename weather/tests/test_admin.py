from django.contrib.admin.sites import AdminSite
from django.urls import reverse

from weather.admin import CityAdmin, WeatherDataAdmin
from weather.models import City, WeatherData
from weather.tests.test_base import WeatherTestBase


class MockRequest:
    pass


class WeatherAdminTest(WeatherTestBase):
    """Test cases for Weather admin interface."""

    def setUp(self):
        super().setUp()
        self.site = AdminSite()
        self.city_admin = CityAdmin(City, self.site)
        self.weather_admin = WeatherDataAdmin(WeatherData, self.site)
        self.request = MockRequest()

    def test_city_admin_list_display(self):
        """Test City admin list display fields."""
        self.assertEqual(
            list(self.city_admin.get_list_display(self.request)),
            ["name", "country", "latitude", "longitude"],
        )

    def test_city_admin_search_fields(self):
        """Test City admin search fields."""
        self.assertEqual(
            list(self.city_admin.get_search_fields(self.request)),
            ["name", "country"],
        )

    def test_city_admin_list_filter(self):
        """Test City admin list filter fields."""
        self.assertEqual(
            list(self.city_admin.get_list_filter(self.request)),
            ["country"],
        )

    def test_weather_admin_list_display(self):
        """Test WeatherData admin list display fields."""
        self.assertEqual(
            list(self.weather_admin.get_list_display(self.request)),
            ["city", "temperature", "weather_condition", "timestamp"],
        )

    def test_weather_admin_list_filter(self):
        """Test WeatherData admin list filter fields."""
        self.assertEqual(
            list(self.weather_admin.get_list_filter(self.request)),
            ["city", "weather_condition", "timestamp"],
        )


class WeatherAdminIntegrationTest(WeatherTestBase):
    """Integration tests for Weather admin interface."""

    def setUp(self):
        super().setUp()
        self.client.force_login(self.admin_user)

    def test_city_admin_list_view(self):
        """Test City admin list view."""
        url = reverse("admin:weather_city_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kyiv")
        self.assertContains(response, "London")

    def test_city_admin_detail_view(self):
        """Test City admin detail view."""
        url = reverse("admin:weather_city_change", args=[self.kyiv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kyiv")
        self.assertContains(response, "Ukraine")

    def test_weather_admin_list_view(self):
        """Test WeatherData admin list view."""
        url = reverse("admin:weather_weatherdata_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kyiv")
        self.assertContains(response, "20.5")

    def test_weather_admin_detail_view(self):
        """Test WeatherData admin detail view."""
        url = reverse("admin:weather_weatherdata_change", args=[self.kyiv_weather.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kyiv")
        self.assertContains(response, "20.5")

    def test_city_admin_search(self):
        """Test City admin search functionality."""
        url = reverse("admin:weather_city_changelist")
        response = self.client.get(url, {"q": "Kyiv"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kyiv")
        self.assertNotContains(response, "London")
