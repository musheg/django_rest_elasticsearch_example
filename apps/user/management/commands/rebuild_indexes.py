from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '''
        Rebuild Elasticsearch indexes
        
        run ./manage rebuild_indexes
    '''

    def handle(self, *args, **options):
        management.call_command('create_indexes', rebuild=True)
