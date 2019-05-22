#!/usr/bin/env python
# coding=utf-8


from django.core.paginator import Paginator
from rest_framework_elasticsearch.es_serializer import ElasticModelSerializer

from apps.user.models import Hashtag
from apps.user.search_indexes import HashtagIndex


class HashtagSerializer(ElasticModelSerializer):
    class Meta:
        es_model = HashtagIndex
        model = Hashtag
        fields = ['name']


class PaginatedSerializer():
    def __init__(self, res, request, num):

        paginator = Paginator(res, num)
        page = request.POST.get('page', 1)
        try:
            p_res = paginator.page(page)
            res = res[num * (page - 1):num]
        except Exception:
            pass
        count = paginator.count
        previous = None if not p_res.has_previous() else p_res.previous_page_number()
        next = None if not p_res.has_next() else p_res.next_page_number()

        self.data = {'count': count, 'previous': previous, 'next': next, 'results': res}
