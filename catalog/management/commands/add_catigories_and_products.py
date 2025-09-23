from django.core.management import call_command
from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Load test data from fixture'

    def handle(self, *args, **kwargs):
        # Delete existing
        Category.objects.all().delete()
        Product.objects.all().delete()

        # Load data from fixtures
        call_command('loaddata', 'catalog_category')
        call_command('loaddata', 'catalog_product')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))