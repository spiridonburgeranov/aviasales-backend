import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aviasales.settings')

app = Celery('aviasales')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'archive-flights-every-minute': {
        'task': 'airlanse_book.tasks.archive_flights',
        'schedule': crontab(hour=0, minute=0)
    },
    'delete-expired-flights-every-month': {
        'task': 'airlanse_book.tasks.delete_expired_flights',
        'schedule': crontab(day_of_month='1', hour=0, minute=0)
    }
}

app.conf.timezone = 'Europe/Moscow'
app.autodiscover_tasks()