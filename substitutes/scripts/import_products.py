"""
IMPORT PRODUCTS

Import products to Open Food Facts database : https://fr.openfoodfacts.org/
This module use Openfoodfacts API : https://en.wiki.openfoodfacts.org/API
"""

import requests, json, re
from substitutes.models import Product


class ImportProducts():

    def __init__(self):
        """
        off_categories   (str ): Json serialize string.
        off_products     (str ): Json serialize string.
        clear_products   (list): Products list.
        """

        self.off_categories = []
        self.off_products = []
        self.clear_products = []

    def auto_products_import(self, language, min_products, category_name):
        """
        This method import products to database.
        """
        self.get_off_categories(language=language, min_products=min_products)
        self.get_off_products(language=language, category_name=category_name)
        self.get_clear_products()
        result = self.send_products_to_database()

        return result

    def get_off_categories(self, language, min_products):
        """
        This method get Openfoodfact categories who have "X" minium products.
        Use request for ask Openfoodfacts API.

        This method take two arguments :

        - language (str): Categories languages ("fr", "en" for example)
        For more informations about Openfoodfacts translation read this :
        https://en.wiki.openfoodfacts.org/Translations

        - min_products (int): Each categories contains "X" products. So if you only
        want to keep categories with at least 20 products. Enter 20 in min_products.
        For more informations about Openfoodfacts categories :
        https://world.openfoodfacts.org/categories

        This method return : A json seralized string.
        """

        if language is None:
            langage = "fr"

        if min_products is None:
            min_products = 100

        request =  requests.get(
            "https://{}.openfoodfacts.org/categories.json".format(language)
        )

        off_json_categories = request.json()
        off_temp_categories = []

        for off_category in off_json_categories['tags']:

            if off_category["products"] >= min_products:
                category = {
                    "id": off_category["id"],
                    "name": off_category["name"],
                    "products": 0
                }
                off_temp_categories.append(category)

        self.off_categories = json.dumps(off_temp_categories)

        return self.off_categories

    def get_off_products(self, language, category_name):
        """
        This method get Openfoodfacts products with category name.

        This method take one argument:

        - category_name(str)  : Openfoodfacts id category name.

        This method return a list of string.
        """

        if language is None:
            langage = "fr"

        # Variable initialization
        off_pages = 0
        request_finish = False

        off_temp_products = []

        page_number = 1
        while request_finish is not True :

            url = "https://{}.openfoodfacts.org/cgi/search.pl".format(language)

            params = {
                'action' : 'process',
                'tagtype_0' : "categories",
                'tag_contains_0' : 'contains',
                'tag_0' : "{}".format(category_name),
                'page_size' : "1000",
                'json' : '1',
                'page' : "{}".format(page_number)
            }

            request = requests.get(url=url, params=params)
            data = request.json()

            for product_dict in data["products"]:

                temp_dict = {
                    "product_name": "",
                    "image_url": "",
                    "url": "",
                    "creator": "",
                    "stores": "",
                    "brands_tags": "",
                    "nutrition_grades": "",
                    "nutriments": "",
                    "categories_hierarchy": "",
                    "ingredients": ""
                }

                for key, value in product_dict.items():

                    for temp_key, temp_value in temp_dict.items():

                        if key == temp_key:

                            temp_dict[temp_key] = value

                off_temp_products.append(temp_dict)

            if page_number == 1:
                products = data["count"]
                if products < 1000:
                    off_pages = 1
                else:
                    off_pages = int(data["count"] / 1000)

            if page_number == off_pages:
                request_finish = True

            page_number += 1

        self.off_products = json.dumps(off_temp_products)

        return self.off_products

    def get_clear_products(self, json_products=None):
        """
        This method take one arguments :
        - json_products(str): json file who represents off products.
        """

        if json_products is None:
            json_products = self.off_products

        products = json.loads(self.off_products)

        import_data = {
            "received_products": 0,
            "accepted_products": 0,
            "rejected_names": 0,
            "rejected_images": 0,
            "rejected_url": 0,
            "rejected_creator": 0,
            "rejected_stores": 0,
            "rejected_brands": 0,
            "rejected_nutriscore": 0,
            "rejected_nutriments_unit_g": 0,
            "rejected_nutriments_energy_unit": 0,
            "rejected_nutriments_energy_kcal": 0,
            "rejected_nutriments_energy_kj": 0,
            "rejected_categories": 0,
            "rejected_ingredients": 0,
        }

        # Settings
        max_lenght_name = 100
        min_lenght_name = 5
        required_image = 0 # 1 for Yes, 0 for No
        default_image = "default.png"
        required_url = 1
        required_creator = 0
        required_stores = 0
        required_brands = 0
        required_nutriscore = 1
        required_categories = 1
        required_energy = 1
        required_energy_kcal = 0
        required_energy_kcal_100g = 0
        required_energy_kj = 0
        required_energy_kj_100g = 0
        required_ingredients = 1

        import_data["received_products"] = len(products)

        for product in products:

            errors = 0

            temp_product = {
                "name": "",
                "image": "",
                "url": "",
                "creator": "",
                "stores": "",
                "brands": "",
                "nutriscore": 0,
                "nutriments": "",
                "categories": "",
                "ingredients": "",
            }

            for key, value in product.items():

                # -- PRODUCT NAME -- #
                if key == "product_name":

                    # Lenght of name
                    if len(str(value)) > max_lenght_name:
                        errors += 1
                        import_data["rejected_names"] += 1
                    elif len(str(value)) < min_lenght_name:
                        errors += 1
                        import_data["rejected_names"] += 1
                    else:
                        temp_product["name"] = value

                # -- PRODUCT IMAGE URL -- #
                elif key == "image_url":

                    if len(str(value)) == 0:
                        if required_image == 1:
                            errors += 1
                            import_data["rejected_images"] += 1
                        else:
                            temp_product["image"] = default_image
                    else:
                        temp_product["image"] = value

                # -- PRODUCT OPENFOODFACTS URL -- #
                elif key == "url":

                    if len(str(value)) == 0:

                        if required_url == 1:
                            errors += 1
                            import_data["rejected_url"] += 1
                        else:
                            temp_product["url"] = "Empty"
                    else:
                        temp_product["url"] = value

                # -- PRODUCT SHEET CREATOR NAME -- #
                elif key == "creator":

                    if len(str(value)) == 0:
                        if required_creator == 1:
                            errors += 1
                            import_data["rejected_creator"] += 1
                        else:
                            temp_product["creator"] = "Unknown"
                    else:
                        temp_product["creator"] = value

                # -- PRODUCT STORE NAMES LIST -- #
                elif key == "stores":

                    if len(str(value)) == 0:
                        if required_stores == 1:
                            errors += 1
                            import_data["rejected_stores"] += 1
                        else:
                            temp_product["stores"] = "Unknown"
                    else:
                        temp_product["stores"] = value

                # -- PRODUCT BRAND NAMES LIST -- #
                elif key == "brands_tags":

                    temp_brands = ",".join(value)

                    if len(str(temp_brands)) == 0:
                        if required_brands == 1:
                            errors += 1
                            import_data["rejected_brands"] += 1
                        else:
                            temp_product["brands"] = ""
                    else:

                        # Remove "-"
                        temp_brands = re.sub(r"-", " ", temp_brands)

                        temp_product["brands"] = temp_brands

                # -- PRODUCT NUTRISCORE VALUE -- #
                elif key == "nutrition_grades":

                    if len(str(value)) == 0:
                        if required_nutriscore == 1:
                            errors += 1
                            import_data["rejected_nutriscore"] += 1
                        else:
                            temp_product["nutriscore"] = 0
                    else:
                        if value == "a":
                            temp_product["nutriscore"] = 1
                        elif value == "b":
                            temp_product["nutriscore"] = 2
                        elif value == "c":
                            temp_product["nutriscore"] = 3
                        elif value == "d":
                            temp_product["nutriscore"] = 4
                        elif value == "e":
                            temp_product["nutriscore"] = 5
                        else:
                            errors += 1

                # -- PRODUCT NUTRIMENTS -- #
                elif key == "nutriments":

                    temp_nutriments = {
                        'carbohydrates': "",
                        'carbohydrates_100g': "" ,
                        'energy_kcal': "",
                        'energy_kcal_100g': "",
                        'energy_kj': "",
                        'energy_kj_100g': "",
                        'fat': "" ,
                        'fat_100g': "",
                        'fiber': "",
                        'fiber_100g': "",
                        'proteins': "",
                        'proteins_100g': "",
                        'salt': "",
                        'salt_100g': "",
                        'saturated-fat': "",
                        'saturated-fat_100g': "",
                        'sodium': "",
                        'sodium_100g': "",
                        'sugars': "",
                        'sugars_100g': "",
                        'sugars_block': ""
                    }

                    # Check "g" unit
                    check = False

                    nutriment_units = (
                        "salt_unit",
                        "saturated-fat_unit",
                        "sodium_unit",
                        "fiber_unit",
                        "sugars_unit",
                        "proteins_unit",
                        "carbohydrates_unit",
                        "fat_unit"
                    )

                    for nutriment_unit in nutriment_units:

                        if value.get(nutriment_unit) == "g":
                            check = True

                    if check is True:

                        # -- ADDITIONNAL ENERGY ACTION -- #
                        energy_unit = value.get("energy_unit")

                        if energy_unit == "kcal":

                            if value.get("energy_kcal") is None:

                                if required_energy_kcal == 1:
                                    errors += 1
                                    import_data["rejected_nutriments_energy_kcal"] += 1
                                else:

                                    value["energy_kcal"] = 0
                                    value["energy_kj"] = 0 * 4.1868

                                if required_energy_kcal_100g == 1:
                                    errors += 1
                                    import_data["rejected_nutriments_energy_kcal_100g"] += 1
                                else:

                                    value["energy_kcal_100g"] = 0
                                    value["energy_kj_100g"] = 0

                            else:

                                value["energy_kcal"] = value.get("energy")
                                value["energy_kj"] = value.get("energy_100g") * 4.1868
                                value["energy_kcal_100g"] = value.get("energy_100g")
                                value["energy_kj_100g"] = value.get("energy_100g") * 4.1868

                        elif energy_unit == "kj":

                            if value.get("energy_kj") is None:

                                if required_energy_kj == 1:
                                    errors += 1
                                    import_data["rejected_nutriments_energy_kj"] += 1
                                else:

                                    value["energy_kcal"] = 0
                                    value["energy_kj"] = 0

                                if required_energy_kj_100g == 1:
                                    errors += 1
                                    import_data["rejected_nutriments_energy_kj_100g"] += 1
                                else:

                                    value["energy_kcal_100g"] = 0
                                    value["energy_kj_100g"] = 0
                            else:

                                    value["energy_kcal"] = value.get("energy") / 4.1868
                                    value["energy_kj"] = value.get("energy")
                                    value["energy_kcal_100g"] = value.get("energy_100g") / 4.1868
                                    value["energy_kj_100g"] = value.get("energy_100g")

                        else:
                            errors += 1
                            import_data["rejected_nutriments_energy_unit"] += 1

                        for key in temp_nutriments.keys():

                            if value.get(key) is None or value.get(key) == "":
                                value_round = 0.0
                            else:
                                value_round = float(value.get(key))

                            temp_nutriments[key] = round(value_round, 2)

                        #-- SUGARS BLOCK --#
                        if value.get('sugars') is None:
                            sugar_value = 0
                        else:
                            sugar_value = float(value.get('sugars'))

                        temp_nutriments['sugars_block'] = int(sugar_value / 5.95)

                        temp_product["nutriments"] = json.dumps(temp_nutriments)

                    else:

                        errors += 1
                        import_data["rejected_nutriments_unit_g"] += 1

                # -- PRODUCT CATEGORIES -- #
                elif key == "categories_hierarchy":

                    temp_categories = ",".join(value)

                    if len(str(temp_categories)) == 0:
                        if required_categories == 1:
                            errors += 1
                            import_data["rejected_categories"] += 1
                        else:
                            temp_product["categories"] = ""
                    else:

                        # Remove for example "fr:", "en:"
                        temp_categories = re.sub(r"[a-zA-Z]*:", "", temp_categories)

                        temp_product["categories"] = temp_categories

                # -- PRODUCT INGREDIENTS -- #
                elif key == "ingredients":

                    if len(value) == 0:
                        if required_ingredients == 1:
                            errors += 1
                            import_data["rejected_ingredients"] += 1
                        else:
                            temp_product["ingredients"] = ""
                    else:

                        temp_product["ingredients"] = json.dumps(value)

            if errors == 0:

                self.clear_products.append(temp_product)

        import_data["accepted_products"] = len(self.clear_products)

        return self.clear_products

    def send_products_to_database(self, products_list=None):
        """
        This method send products to database with Django ORM.

        This method take one argument :
        - products_list(list): Products list.

        This method return a tupple (
            nbr of products in list, nbr of products add in db
        )
        """

        if products_list is None:
            products_list = self.clear_products

        for product in products_list:

            new_product = Product(
                name = product['name'],
                image = product['image'],
                url = product['url'],
                creator = product['creator'],
                brands = product['brands'],
                stores = product['stores'],
                nutriscore = product['nutriscore'],
                categories = product['categories'],
                ingredients = product['ingredients'],
                nutriments = product['nutriments']
            )

            new_product.save()

        db_products = Product.objects.all()

        return (len(products_list), len(db_products))
