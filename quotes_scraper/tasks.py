from random import choice, choices

from celery import shared_task
import requests
import time

from django.db.models import Count

from django_celery.celery import BaseTaskWithRetry
from quotes_scraper.models import Quote
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(bind=True, base=BaseTaskWithRetry)
def scrape_quote(self):
    logger.info(f"Task {self.request.id} started.")

    # Add random delay for testing
    time.sleep(choice(range(10)))

    # Randomly generate Exception (probability 1/50)
    if choices([True, False], [1, 10])[0]:
        raise Exception("Random exception!")

    # Api to fetch quotes
    response = requests.get("https://goquotes-api.herokuapp.com/api/v1/random?count=1")
    if not response.ok:
        raise Exception("Failed to fetch quote. Error:" + response.text)

    quotes = response.json().get("quotes")
    if quotes is None:
        logger.warning("No quotes available in response.")
    quote_objs = []
    for q in quotes:
        quote_objs.append(Quote(quote=q["text"], author=q["author"]))
    Quote.objects.bulk_create(quote_objs)

    logger.info(f"Task {self.request.id}: {len(quote_objs)} quotes added.")

@shared_task(bind=True)
def find_duplicate_quotes(self):
    logger.info(f"Task {self.request.id} started.")
    duplicate_quotes = Quote.objects.values("quote", "author").annotate(d_count=Count("id")).order_by().filter(d_count__gt=1)
    logger.info(f"{self.request.id} task: {len(duplicate_quotes)} duplicate quotes found")

    # <Code to remove duplicates>
    return duplicate_quotes
