from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product
from users.models import Profile


class IndexPageTestCase(TestCase):
    # test that index page returns a 200
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class LegaleNoticePageTestCase(TestCase):
    # test that legale notice page returns a 200
    def test_legale_notice_page_returns_200(self):
        response = self.client.get(reverse('legales_notices'))
        self.assertEqual(response.status_code, 200)

class UserPageTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username = "tester",
            email = "test@test.fr",
            password = "testing",
        )
        cls.user_profile = Profile(user=cls.user)

    def test_login_page_returns_200(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_page_returns_200(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_returns_200(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_profile_page_returns_200(self):
        # connection ON
        user = self.client.login(username="test", password="testing")
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/profile/')

    def test_profile_page_returns_302(self):
        # connection OFF
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/profile/')

class ProductPageTestCase(TestCase):
    # Test that product page returns a 200 if the item exists.

    def test_product_page_returns_200(self):
        product = Product.objects.create(
            product_name = "Nutella",
            product_brands = "Ferrero",
            product_url = "https://fr.openfoodfacts.org/produit/3017620429484/nutella-ferrero",
            product_creator = "openfoodfacts-contributors",
            product_nutriscore = "e",
            product_image_url = "https://static.openfoodfacts.org/images/products/301/762/042/9484/front_fr.204.full.jpg",
            product_kcal = 544,
            product_kj = 2278,
            product_sugar = 56.8,
            product_saturated_fat = 11,
            product_fat = 31.6,
            product_salt = 0.114,
            product_nova = 4,
            product_categories = "Produits à tartiner, Petit-déjeuners, Produits à tartiner sucrés, Pâtes à tartiner, Pâtes à tartiner aux noisettes, Pâtes à tartiner au chocolat, Pâtes à tartiner aux noisettes et au cacao",
        )

        response = self.client.get(reverse("product", args=[product.pk]))
        self.assertEqual(response.status_code, 200)
