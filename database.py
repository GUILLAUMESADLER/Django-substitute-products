
class database():
    """
    """

    def get_products(self, keyword=None):
        """ We take an keyword, per example 'Nutella'.
            We check in database if one or more product title contain keyword.
            We return a list of lists who contain products found. """

        if keyword is not None:
            pass

        return products

    def get_substitutes(self, product_id=None):
        """ This method return product
        """

        pass

    def save_product(self, username=None, product_id=None):
        """ """
        user = User.objects.get(username=username)
        product = Product.objects.get(id=product_id)

        # user.profile.products.add(product.id)


