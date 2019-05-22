#!/usr/bin/env python
# coding=utf-8
import logging

from rest_framework import serializers
from rest_framework_elasticsearch.es_serializer import ElasticModelSerializer

from apps.user.models import Product
from apps.user.search_indexes import ProductIndex

logger = logging.getLogger(__name__)


class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'primary_picture',
            'id',
            'url'
        ]


class ProductSerializer(ElasticModelSerializer):
    pictures = serializers.SerializerMethodField()

    class Meta:
        es_model = ProductIndex
        model = Product
        fields = [
            'name',
            'primary_picture',
            'id',
            'url',
            'pictures'
        ]

    def get_pictures(self, obj):
        request = self.context.get('request', None)
        return [request.build_absolute_uri(pp.picture.url) for pp in obj.pictures.all()]
