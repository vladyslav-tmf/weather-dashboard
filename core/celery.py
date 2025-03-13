import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("weather_dashboard")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "update-weather-data-hourly": {
        "task": "weather.tasks.schedule_weather_updates_for_all_cities",
        "schedule": crontab(minute=0),
    },
}
