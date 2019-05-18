import requests
from search.models import Product

class OffManager():

    def __init__(self):

        self.products_list = []
        self.get_products()
        self.fill_db()

    def get_products(self):
        """ This method get all product of produits-a-tartiner-sucres
        off category """

        # Initialization
        off_pages = 0
        request_finish = False

        page_number = 1
        while request_finish is not True :

            url = "https://fr.openfoodfacts.org/cgi/search.pl"

            params = {
                'action' : 'process',
                'tagtype_0' : "categories",
                'tag_contains_0' : 'contains',
                'tag_0' : "produits-a-tartiner-sucres",
                'page_size' : "1000",
                'json' : '1',
                'page' : "{}".format(page_number)
            }

            request = requests.get(url=url, params=params)
            data = request.json()

            if page_number == 1:
                products = data["count"]
                if products < 1000:
                    off_pages = 1
                else:
                    off_pages = int(data["count"] / 1000)

            if page_number == off_pages:
                request_finish = True

            self.product_treatment(products=data)

            page_number += 1

    def product_treatment(self, products=None):

        for product in products["products"]:

            err = 0
            product_dict = {}

            # -- NAME OF PRODUCT -- #
            try:

                product_name = str(product["product_name"])
                if len(product_name) > 25:
                    err += 1

            except Exception as e:
                product_name = "empty"

            # -- URL OF PRODUCT -- #
            try:
                product_url = str(product["url"])
            except Exception as e:
                err += 1

            # -- NAME OF CREATOR PRODUCT SHEET -- #
            try:
                product_creator = str(product["creator"])
            except Exception as e:
                product_creator = "empty"

            # -- STORES NAME OF PRODUCTS -- #
            try:
                product_stores = str(product["stores"])
            except Exception as e:
                product_stores = "empty"


            # -- NUTRITION GRADE VALUE -- #
            try:
                product_nutriscore = str(product["nutrition_grades"])
            except Exception as e:
                err += 1

            # -- IMAGE URL OF PRODUCT -- #
            try:
                product_image_url = str(product["image_url"])
            except Exception as e:
                err += 1

            # -- ENERGY OF PRODUCT -- #
            try:
                energy = str(product["nutriments"]["energy_unit"])
                energy_value = int(
                    product["nutriments"]["energy_100g"]
                )

                if energy.lower() == "kcal":
                    product_kj = energy_value * 4.1868
                    product_kcal = energy_value
                elif energy.lower() == "kj":
                    product_kj = energy_value
                    product_kcal = energy_value / 4.1868

            except Exception as e:
                err += 1

            # -- SUGAR VALUE -- #
            try:
                product_sugar = float(product["nutriments"]["sugars_100g"])
            except Exception as e:
                err += 1

            # -- SATURED FAT VALUE -- #
            try:
                saturated_fat = float(product["nutriments"]["saturated_fat"])
            except Exception as e:
                saturated_fat = 0

            # -- FAT VALUE -- #
            try:
                fat = float(product["nutriments"]["fat"])
            except Exception as e:
                fat = 0

            # -- SALT VALUE -- #
            try:
                salt = float(product["nutriments"]["salt"])
            except Exception as e:
                salt = 0

            # -- NOVA VALUE -- #
            try:
                nova = int(product["nutriments"]["nova-group_serving"])
            except Exception as e:
                nova = 0

            # -- SUGAR VALUE -- #
            try:
                product_sugar = float(product["nutriments"]["sugars_100g"])
            except Exception as e:
                product_sugar = 0

            # -- BRANDS TAGS OF PRODUCTS -- #
            try:
                brands_list = product["brands_tags"]
                product_brands = ",".join(brands_list)
            except Exception as e:
                err += 1

            # -- CATEGORIES OF PRODUCTS -- #
            try:
                product_categories = product["categories"]
            except Exception as e:
                err += 1

            if err == 0:

                product_dict["product_name"] = product_name
                product_dict["product_url"] = product_url
                product_dict["product_creator"] = product_creator
                product_dict["product_stores"] = product_stores
                product_dict["product_nutriscore"] = product_nutriscore
                product_dict["product_image_url"] = product_image_url
                product_dict["product_kj"] = product_kj
                product_dict["product_kcal"] = product_kcal
                product_dict["product_sugar"] = product_sugar
                product_dict["product_saturated_fat"] = saturated_fat
                product_dict["product_fat"] = fat
                product_dict["product_salt"] = salt
                product_dict["product_nova"] = nova
                product_dict["product_brands"] = product_brands
                product_dict["product_categories"] = product_categories

                self.products_list.append(product_dict)

    def fill_db(self):
        """
        """

        for product in self.products_list:

            new_product = Product(
                product_name = product['product_name'],
                product_brands = product['product_brands'],
                product_url = product['product_url'],
                product_creator = product['product_creator'],
                product_nutriscore = product['product_nutriscore'],
                product_image_url = product['product_image_url'],
                product_kcal = product['product_kcal'],
                product_kj = product['product_kj'],
                product_sugar = product['product_sugar'],
                product_saturated_fat = product['product_saturated_fat'],
                product_fat = product['product_fat'],
                product_salt = product['product_salt'],
                product_nova = product['product_nova'],
                product_categories = product['product_categories'],
            )

            new_product.save()

