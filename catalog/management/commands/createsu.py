import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser from .env variables if it does not exist.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv('SU_USERNAME', 'admin')
        email = os.getenv('SU_EMAIL', 'admin@example.com')
        password = os.getenv('SU_PASSWORD', 'admin')
        
        if not User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Creating superuser: {username}'))
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))
