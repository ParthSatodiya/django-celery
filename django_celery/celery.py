import os

from celery import Celery
from celery import Task

# Set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery.settings')

app = Celery('django_celery')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

class BaseTaskWithRetry(Task):
    autoretry_for = (Exception,)
    max_retries = 2
    retry_backoff = True
    retry_backoff_max = 700
    default_retry_delay=60

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-10-seconds': {
        'task': 'quotes_scraper.tasks.find_duplicate_quotes',
        'schedule': 10.0,
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
