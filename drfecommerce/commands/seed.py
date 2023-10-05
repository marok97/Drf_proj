from typing import Any
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "seed db for testing and development"

    def add_arguments(self, parser ) -> None:
        parser.add_argument("--mode", type=str, help="Mode")
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write("seeding database...")
        run_seed(self, options["mode"])
        self.stdout.write("Done...")


def create_categories():
    print("Creating categories....")
    category_names = [""]

def create_brand():
    pass

def create_products():
    pass

def run_seed(self, mode):
    pass