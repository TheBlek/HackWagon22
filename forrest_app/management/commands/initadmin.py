from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.count() == 0:
            print('Creating admin account')
            User.objects.create_superuser('admin', 'admin@gmail.com', 'admin').save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
