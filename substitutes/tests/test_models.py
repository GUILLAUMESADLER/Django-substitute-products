from django.test import TestCase
from substitutes.models import Product

class ProductTestCase(TestCase):

    def setUp(self):

        Product.objects.create(
            name = "Andouille non fumée",
            image = "https://static.openfoodfacts.org/images/products/325/039/092/8300/front_fr.9.400.jpg",
            url = "https://fr.openfoodfacts.org/produit/3250390928300/andouille-non-fumee-netto",
            creator = "jacob80",
            brands = "netto,les mousquetaires",
            stores = "Netto",
            nutriscore = 5,
            categories = "meats,prepared-meats,fresh-foods,saucissons,andouilles,saucissons-cuits",
            ingredients = '[{"rank": 1, "text": "Chaudins", "id": "fr:Chaudins"}, {"text": "rosettes", "id": "fr:rosettes", "rank": 2}, {"rank": 3, "id": "fr:gras-et-couenne-de-porc", "text": "gras et couenne de porc"}, {"rank": 4, "text": "sel", "id": "en:salt"}, {"text": "\u00e9pices", "id": "en:spice", "rank": 5}, {"rank": 6, "id": "en:spice", "text": "aromates"}, {"rank": 7, "text": "conservateur", "id": "en:preservative"}, {"text": "nitrite de sodium", "id": "fr:nitrite-de-sodium", "rank": 8}, {"rank": 9, "id": "en:flavouring", "text": "ar\u00f4mes"}]',
            nutriments = '{"carbohydrates": "", "carbohydrates_100g": "", "energy_kcal": "", "energy_kcal_100g": "", "energy_kj": "", "energy_kj_100g": "", "fat": "", "fat_100g": "", "fiber": "", "fiber_100g": "", "proteins": "", "proteins_100g": "", "salt": "", "salt_100g": "", "saturated-fat": "", "saturated-fat_100g": "", "sodium": "", "sodium_100g": "", "sugars": "", "sugars_100g": "", "sugars_block": ""}',
        )
