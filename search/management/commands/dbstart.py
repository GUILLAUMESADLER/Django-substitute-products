import requests
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from search.models import Product
from off import OffManager


class Command(BaseCommand):
    print("Udpate database")

    def handle(self, *args, **options):
        Product.objects.all().delete()

        OffManager()
