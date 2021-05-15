import os, json

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from user.models import User
from member.models import Team, Member

class Command(BaseCommand):
    help = '重置或生成假user数据'

    def handle(self, *args, **options):
        commands_path = os.path.abspath(os.path.dirname(__file__))
        with open(commands_path + '/fakememberdata.json', encoding='utf-8') as f:
            fake_data = json.load(f)
        for fake in fake_data['Team']:
            team, created = Team.objects.update_or_create(
                name_ch=fake['name_ch'],
                defaults=fake
            )
        for fake in fake_data['Member']:
            email = fake.pop('email')
            if not User.objects.filter(email=email).exists():
                raise CommandError(f'未找到email为{email}的user')
            fake['user'] = User.objects.get(email=email)
            member, created = Member.objects.update_or_create(
                user__email=email,
                defaults=fake
            )
