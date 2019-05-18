import requests
from django.core.management.base import BaseCommand, CommandError
from substitutes.models import Product
from substitutes.scripts.import_products import ImportProducts


class Command(BaseCommand):

    help = 'Import Openfoodfacts products to database'

    def handle(self, *args, **options):

        # Delete all database products
        Product.objects.all().delete()

        # Import products to database
        new_product_import = ImportProducts()

        products = new_product_import.auto_products_import(
            language="fr",
            min_products=100,
            category_name="produits-a-tartiner-sucres"
        )

        self.stdout.write('Nombres de produits importés : {}'.format(len(products)))
