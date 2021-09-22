# django-celery
This is an [Celery](https://docs.celeryproject.org/) example in django project with docker environment.

It is using [postgres](https://www.postgresql.org/) as django project database and [redis](https://redis.io/) as message broker in celery.

Run this project with docker using `docker-compose up` which will start **postgres** database, **redis** borker, celery **worker**, celery **beat** scheduler and django **example app**. 
