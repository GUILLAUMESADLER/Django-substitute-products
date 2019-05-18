from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_brands = models.CharField(max_length=100)
    product_url = models.URLField(max_length=300)
    product_creator = models.CharField(max_length=100)
    product_nutriscore = models.CharField(max_length=10)
    product_image_url = models.URLField(max_length=300)
    product_kcal = models.IntegerField()
    product_kj = models.IntegerField()
    product_sugar = models.FloatField()
    product_saturated_fat = models.FloatField()
    product_fat = models.FloatField()
    product_salt = models.FloatField()
    product_nova = models.IntegerField()
    product_categories = models.CharField(max_length=500)

    class Meta:
        verbose_name = "products"
        ordering = ['product_name']

    def __str__(self):
        """
        """
        return self.product_name
