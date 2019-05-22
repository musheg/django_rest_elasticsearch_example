#!/usr/bin/env python
# coding=utf-8

# https://stackoverflow.com/questions/31483282/django-rest-framework-combining-routers-from-different-apps
from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

# router = SimpleRouter()
from apps.user.views.account import UserViewSet, FollowerView, FollowingView
from apps.user.views.feed import HashtagViewSet
from apps.user.views.products import ProductViewSet
from apps.user.views.search import SearchAPIView

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('products', ProductViewSet)
router.register('hashtags', HashtagViewSet)

urlpatterns = [
    url('', include(router.urls)),
    url(r'^followers/$', FollowerView.as_view()),
    url(r'^following/$', FollowingView.as_view()),
    url(r'^search/$', SearchAPIView.as_view()),
]
