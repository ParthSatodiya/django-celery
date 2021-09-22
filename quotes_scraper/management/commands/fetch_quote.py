from django.core.management import BaseCommand

from quotes_scraper.tasks import scrape_quote


class Command(BaseCommand):
    help = "Add task to fetch quotes"

    def add_arguments(self, parser):
        parser.add_argument("num_quote", type=int)

    def handle(self, *args, **options):
        num_quote = options["num_quote"]
        self.stdout.write(f"Adding tasks to fetch {num_quote} quotes...")
        for i in range(num_quote):
            scrape_quote.apply_async(ignore_result=True)
        self.stdout.write("Tasks added successfully.")
