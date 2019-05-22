from django.conf import settings
from elasticsearch_dsl import DocType, Integer, Text, Date, Keyword

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=[settings.ELASTIC_URL])

class UserIndex(DocType):
    """
    Get more control over the mapping, see
    curl -X GET "localhost:9200/user/_mapping?pretty"
    """
    pk = Integer()
    username = Text(fields={'raw': Keyword()})
    email = Text()
    full_name = Text()
    gender = Text()
    description = Text()
    date_joined = Date()
    age = Integer()

    class Meta:
        index = 'user'


class HashtagIndex(DocType):
    pk = Integer()
    name = Text(fields={'raw': Keyword()})

    class Meta:
        index = 'hashtag'


class ProductIndex(DocType):
    pk = Integer()
    name = Text(fields={'raw': Keyword()})
    description = Text()

    class Meta:
        index = 'product'


SEARCH_INDEXES = [
    {
        'index': 'user',
        'model': 'User',
        'es_model': UserIndex,
    },
    {
        'index': 'hashtag',
        'model': 'Hashtag',
        'es_model': HashtagIndex,
    }, {
        'index': 'product',
        'model': 'Product',
        'es_model': ProductIndex,
    }
]
