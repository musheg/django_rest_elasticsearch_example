from django.apps import apps
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from apps.user.search_indexes import SEARCH_INDEXES
from apps.user.serializers.accounts import PublicUserSerializer
from apps.user.serializers.discovery import HashtagSerializer
from apps.user.serializers.products import ProductSerializer


class Command(BaseCommand):
    help = '''
        Create not existing Elasticsearch indexes

        run ./manage create_indexes
    '''

    def _get_req_ctx(self):
        """
        Hyperlinked serializers need request in context
        """
        factory = APIRequestFactory()
        request = factory.get('/', SERVER_NAME=Site.objects.get_current().domain)
        return {'request': Request(request), }

    def add_arguments(self, parser):
        parser.add_argument(
            '--rebuild',
            action='store_true',
            dest='rebuild',
            help='Rebuild all indexes (delete existing indexes)'
        )

    def handle(self, *args, **options):
        es = Elasticsearch()

        if options['rebuild']:
            for index in es.indices.get_alias():
                es.indices.delete(index)

        serializer_map = {'User': PublicUserSerializer,
                          'Hashtag': HashtagSerializer,
                          'Product': ProductSerializer}
        for index in SEARCH_INDEXES:
            if not es.indices.exists(index['index']):
                index['es_model'].init()
                for inst in apps.get_model('user', index['model']).objects.all().iterator():
                    print(index)
                    obj = serializer_map[index['model']](inst, context=self._get_req_ctx())
                    obj.save()
