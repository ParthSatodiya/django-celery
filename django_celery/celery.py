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
        'schedule': 30.0,
    },
}

# @app.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#
#     # Executes find_duplicate_quotes every 10 seconds
#     sender.add_periodic_task(10.0, quotes_scraper.tasks.find_duplicate_quotes.delay())

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
