# django-celery
This is an example of [Celery](https://docs.celeryproject.org/) integration in django app with docker environment.

### Run example locally
Clone the repository and inside the directory, run following commands
```shell
cp .env.example .env
docker compose up
```
This will build the app image if necessary and spin up following containers:
- [**postgres**]((https://www.postgresql.org/)) container for app database
- **app** container which will perform migration first and start local django server on port `8000`
- [**redis**](https://redis.io/) container used as a [message broker](https://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#choosing-a-broker) for celery
- **celery_worker** container for [celery worker](https://docs.celeryproject.org/en/latest/userguide/workers.html)
- **celery_beat** container for celery [beat scheduler](https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html)

App follows simple django-celery configuration described in [celery documentation](https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html).
Which means most of the celery configuration like creating celery app, custom task/queue configuration, celery beat schedules are in `./django_celery/celery.py` file and some additional configuration like broker url etc in settings.py file with `CELERY_` prefix.
```shell
CELERY_TIMEZONE = "UTC"
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
```

Django app mainly has 2 tasks to perform:
1. Fetch quotes from the internet along with quote author and store it in the database
    - This is considered as on demand task which means some external event will queue this task and it will be executed later by celery worker.
    - In this case, external event is a django custom management command `fetch_quote`.
      ```shell
      docker compose exec app python manage.py fetch_quote
      ```
    - This will push this task in celery queue for worker to execute


2. Find duplicate quotes stored in the database (as if we want to delete the duplicate quotes)
    - This will simulate scheduled task with celery. App is using default celery beat scheduler which will queue tasks based on it's scheduled time.
    - This particular task is scheduled to be queued every 10 seconds.

For fetching quotes from the internet, app is using [goquotes](https://goquotes.docs.apiary.io/#reference) public api ([github repo](https://github.com/amsavarthan/goquotes-api)).
