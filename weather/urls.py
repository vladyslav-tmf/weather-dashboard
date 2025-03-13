from rest_framework.routers import DefaultRouter

from weather.views import CityViewSet, WeatherDataViewSet

router = DefaultRouter()
router.register("cities", CityViewSet, basename="cities")
router.register("weather", WeatherDataViewSet, basename="weather")

urlpatterns = router.urls
