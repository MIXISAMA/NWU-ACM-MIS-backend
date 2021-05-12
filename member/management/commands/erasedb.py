from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os

def remove_and_display(path):
    if os.path.isdir(path):
        for file_name in os.listdir(path):
            remove_and_display(path / file_name)
        os.rmdir(path)
    else:
        os.remove(path)
    print('removed', path)

class Command(BaseCommand):
    help = 'delete all migrations script files, and delete db.sqlite3 file'

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR
        db_path = base_dir / 'db.sqlite3'
        if os.path.exists(db_path):
            remove_and_display(db_path)

        for file_name in os.listdir(base_dir):

            migrations_path = base_dir / file_name / 'migrations/'
            if not os.path.exists(migrations_path):
                continue
            
            pycache_path = migrations_path / '__pycache__'
            if os.path.exists(pycache_path):
                remove_and_display(pycache_path)

            for x in os.listdir(migrations_path):

                if x == '__init__.py':
                    continue
                remove_and_display(migrations_path / x)
