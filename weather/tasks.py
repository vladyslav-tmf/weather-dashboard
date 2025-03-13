import logging

from celery import shared_task
from httpx import HTTPError

from weather.models import City
from weather.services import WeatherService

logger = logging.getLogger(__name__)


@shared_task(
    name="fetch_and_update_city_weather", max_retries=3, default_retry_delay=300
)
def fetch_and_update_city_weather(city_id: int) -> bool:
    """
    Asynchronous fetch and update weather data for a specific city.
    Returns True if weather was successfully updated, False otherwise.
    """
    try:
        city = City.objects.get(id=city_id)
        service = WeatherService()
        weather = service.update_weather_for_city(city)

        if weather:
            logger.info(
                f"Successfully updated weather for {city.name}: {weather.temperature}°C"
            )
            return True

        logger.error(f"Failed to update weather for {city.name}")
        return False

    except City.DoesNotExist:
        logger.error(f"City with id {city_id} not found")
        return False
    except HTTPError as error:
        logger.error(f"HTTP error while updating weather for {city_id}, {error}")
        return False
    except (ValueError, KeyError) as error:
        logger.error(
            f"Data processing error while updating weather for {city_id}, {error}"
        )
        return False


@shared_task(
    name="schedule_weather_updates_for_all_cities",
    max_retries=3,
    default_retry_delay=300,
)
def schedule_weather_updates_for_all_cities() -> int:
    """
    Schedule asynchronous weather updates for all cities in the database.
    Returns the number of cities scheduled for update.
    """
    cities = City.objects.all()
    scheduled_count = 0

    for city in cities:
        try:
            fetch_and_update_city_weather.delay(city.id)
            scheduled_count += 1
            logger.info(f"Scheduled weather update for {city.name}")

        except (ValueError, HTTPError) as error:
            logger.error(f"Failed to schedule weather update for {city.name}, {error}")

    logger.info(f"Scheduled weather updates for {scheduled_count} cities")
    return scheduled_count
