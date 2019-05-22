#!/usr/bin/env python
# coding=utf-8

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.user.models import Product
from apps.user.serializers.products import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = Product.objects.all().prefetch_related('pictures', 'supplier_info', 'supplier_info__supplier')
        # return Product.objects.all().prefetch_related('pictures')
        return qs
