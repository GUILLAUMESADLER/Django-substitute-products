from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):

    help = 'Super user list'

    def handle(self, *args, **options):

        superusers = User.objects.filter(is_superuser=True)
        superusers_emails = User.objects.filter(is_superuser=True).values_list('email')

        print(superusers_emails)
