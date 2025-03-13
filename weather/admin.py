from django.contrib import admin

from weather.models import City, WeatherData


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "latitude", "longitude"]
    search_fields = ["name", "country"]
    list_filter = ["country"]


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ["city", "temperature", "weather_condition", "timestamp"]
    list_filter = ["city", "weather_condition", "timestamp"]
    date_hierarchy = "timestamp"
