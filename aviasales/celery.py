import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aviasales.settings')

app = Celery('aviasales')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'archive-flights-every-minute': {
        'task': 'airlanse_book.tasks.archive_flights',
        'schedule': crontab(minute='0,30')
    },
}

app.conf.timezone = 'Europe/Moscow'
app.autodiscover_tasks()