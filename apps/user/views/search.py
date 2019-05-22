#!/usr/bin/env python
# coding=utf-8

from django.conf import settings
from elasticsearch import Elasticsearch, RequestsHttpConnection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_elasticsearch import es_views, es_filters

from apps.user.search_indexes import UserIndex, HashtagIndex, ProductIndex


class SearchFilter(es_filters.ElasticSearchFilter):
    search_param = 'q'


filter_backends = (
    es_filters.ElasticFieldsFilter,
    SearchFilter
)


class UserSearchView(es_views.ListElasticAPIView):
    es_client = Elasticsearch(hosts=[settings.ELASTIC_URL], connection_class=RequestsHttpConnection)
    es_model = UserIndex
    es_filter_backends = filter_backends
    # These fields will be searchable with q multimatch and need 75% match by default
    # ./get 'v1/search/?topic=users&q=whatever.com'
    es_search_fields = ('username', 'full_name', 'email', 'description')


class HashtagSearchView(es_views.ListElasticAPIView):
    es_client = Elasticsearch(hosts=[settings.ELASTIC_URL], connection_class=RequestsHttpConnection)
    es_model = HashtagIndex
    es_filter_backends = filter_backends
    es_search_fields = ('name',)


class ProductSearchView(es_views.ListElasticAPIView):
    es_client = Elasticsearch(hosts=[settings.ELASTIC_URL], connection_class=RequestsHttpConnection)
    es_model = ProductIndex
    es_filter_backends = filter_backends
    es_search_fields = ('name', 'description', 'supplier_info.name', 'supplier_info.supplier.name')


SEARCH_VIEWS = {
    'users': UserSearchView.as_view(),
    'hashtags': HashtagSearchView.as_view(),
    'products': ProductSearchView.as_view()
}


class SearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        topic = request.GET.get('topic')

        if not topic or topic not in SEARCH_VIEWS.keys():
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'Please specify a valid topic'})

        return SEARCH_VIEWS[topic](self.request._request, *args, **kwargs)
