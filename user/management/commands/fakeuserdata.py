import os, json

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from user.models import User

class Command(BaseCommand):
    help = '重置或生成假user数据'

    def handle(self, *args, **options):
        commands_path = os.path.abspath(os.path.dirname(__file__))
        with open(commands_path + '/fakeuserdata.json', encoding='utf-8') as f:
            fake_data = json.load(f)
        for fake in fake_data:
            user, created = User.objects.update_or_create(
                email=fake['email'],
                defaults=fake
            )
            user.set_unusable_password()
