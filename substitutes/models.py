"""
PRODUCTS models
"""

from django.db import models

class Product(models.Model):

    name = models.CharField(max_length=100)
    image = models.URLField(max_length=300)
    url = models.URLField(max_length=300)
    creator = models.CharField(max_length=100)
    brands = models.CharField(max_length=100)
    stores = models.TextField()
    nutriscore = models.IntegerField()
    categories = models.TextField()
    ingredients = models.TextField()
    nutriments = models.TextField()

    class Meta:
        verbose_name = "product"
        ordering = ['name']

    def __str__(self):
        return self.name
