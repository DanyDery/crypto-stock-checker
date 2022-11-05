from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_stock.settings')

app = Celery('crypto_stock')
app.conf.enable_utc = False
app.conf.update(timezone='Europe/Kiev')

app.config_from_object(settings, namespace='CELERY')

app.conf.beat_scheduler = {
    'every-10-seconds': {
        'task': 'tracker.task.update_stock',
        'schedule': 10,
        'args': ('AAPL')  # ??
    },
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
