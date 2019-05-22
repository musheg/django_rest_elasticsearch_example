#!/usr/bin/env python
# coding=utf-8

from collections import namedtuple

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.user.models import Hashtag
from apps.user.serializers.discovery import HashtagSerializer

FeedSerializationInfo = namedtuple('FeedSerializationInfo', ['serializer_class', 'type_name'])


class HashtagViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = (IsAuthenticated,)
