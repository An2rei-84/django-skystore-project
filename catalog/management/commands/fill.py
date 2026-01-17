from django.core.management import call_command
from django.core.management.base import BaseCommand
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Deletes all data from Product and Category tables and loads new data from fixtures.'

    def handle(self, *args, **options):
        # Удаление всех продуктов и категорий
        self.stdout.write(self.style.WARNING('Deleting all products and categories...'))
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All products and categories have been deleted.'))

        # Загрузка данных из фикстур
        self.stdout.write(self.style.WARNING('Loading data from fixtures...'))
        call_command('loaddata', 'catalog/fixtures/categories.json')
        call_command('loaddata', 'catalog/fixtures/products.json')
        self.stdout.write(self.style.SUCCESS('Data has been successfully loaded from fixtures.'))