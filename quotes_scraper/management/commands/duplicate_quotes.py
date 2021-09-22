from django.core.management import BaseCommand

from quotes_scraper.tasks import scrape_quote, find_duplicate_quotes


class Command(BaseCommand):
    help = "Find duplicate quotes"

    def handle(self, *args, **options):
        self.stdout.write(f"Adding tasks to find duplicate quotes...")
        find_duplicate_quotes.apply_async(retry=True)
        self.stdout.write("Tasks added successfully.")
