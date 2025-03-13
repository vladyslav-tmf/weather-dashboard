from django.conf import settings
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    country = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    external_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ["name"]
        indexes = [models.Index(fields=["name", "country"])]

    def __str__(self) -> str:
        return f"{self.name}, {self.country}"


class WeatherData(models.Model):
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="weather_data"
    )
    temperature = models.FloatField()
    feels_like = models.FloatField()
    humidity = models.PositiveSmallIntegerField()
    pressure = models.PositiveSmallIntegerField()
    wind_speed = models.FloatField()
    wind_direction = models.PositiveSmallIntegerField()
    weather_condition = models.CharField(max_length=255, db_index=True)
    weather_description = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-timestamp"]
        get_latest_by = "timestamp"
        indexes = [models.Index(fields=["city", "timestamp"])]

    def __str__(self) -> str:
        unit = "°C" if settings.OPEN_WEATHER_MAP_API_UNITS == "metric" else "°F"
        return f"{self.city.name}: {self.temperature}{unit} at {self.timestamp}"
