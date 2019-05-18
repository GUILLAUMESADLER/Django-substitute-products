"""
For more informations about django test :
https://docs.djangoproject.com/en/2.2/topics/testing/overview/

"""
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.test import TestCase, Client
from django.urls import reverse
from substitutes.models import Product

class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username = "test",
            email = "test@test.com",
            password = "testing"
        )
        cls.product = Product.objects.create(
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

    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'substitutes/index.html')

    def test_results(self):
        response = self.client.post(
            reverse("results"), {
                'product-name': 'Bananne'
            }
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'substitutes/result.html')

    @login_required
    def test_favorites_connected(self):
        self.client.login(username="test", password="testing")
        response = self.client.get(reverse("favorites"))
        self.assertEquals(response.status_code, 200)

    @login_required
    def test_favorites_no_connected(self):
        response = self.client.get(reverse("favorites"))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/favorites')

    @login_required
    def test_add_favorite_connected(self):
        self.client.login(username="test", password="testing")
        response = self.client.get(reverse("add_favorite", args=[1]))
        self.assertEquals(response.status_code, 200)

    @login_required
    def test_add_favorite_no_connected(self):
        response = self.client.get(reverse("add_favorite", args=[1]))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/add_favorite/1')

    @login_required
    def test_del_favorite_connected(self):
        self.client.login(username="test", password="testing")
        response = self.client.get(reverse("del_favorite", args=[1]))
        self.assertEquals(response.status_code, 200)

    @login_required
    def test_del_favorite_no_connected(self):
        response = self.client.get(reverse("del_favorite", args=[1]))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/del_favorite/1')

    def test_substitutes(self):
        response = self.client.get(reverse("substitutes", args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'substitutes/sub_result.html')

    def test_legales_notices(self):
        response = self.client.get(reverse("legales_notices"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'substitutes/legales_notices.html')

    def test_product(self):
        response = self.client.get(reverse("product", args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'substitutes/product.html')
