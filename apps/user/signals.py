from django.contrib.sites.models import Site
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from apps.user.models import User, Hashtag, Product
from apps.user.serializers.accounts import PublicUserSerializer
from apps.user.serializers.discovery import HashtagSerializer
from apps.user.serializers.products import ProductSerializer


def _get_req_ctx():
    """
    Hyperlinked serializers need request in context
    """
    factory = APIRequestFactory()
    request = factory.get('/', SERVER_NAME=Site.objects.get_current().domain)
    return {'request': Request(request), }


@receiver(post_save, sender=User, dispatch_uid="update_user_index")
def update_es_user_record(sender, instance, **kwargs):
    request_ctx = kwargs.get('request_ctx', _get_req_ctx())
    obj = PublicUserSerializer(instance, context=request_ctx)
    obj.save()


@receiver(post_delete, sender=User, dispatch_uid="delete_user_index")
def delete_es_user_record(sender, instance, *args, **kwargs):
    # N.B User videos would have to have been deleted already anyway
    request_ctx = kwargs.get('request_ctx', _get_req_ctx())
    obj = PublicUserSerializer(instance, context=request_ctx)
    obj.delete(ignore=404)


@receiver(post_save, sender=Hashtag, dispatch_uid="update_hashtag_index")
def update_es_hashtag_record(sender, instance, **kwargs):
    obj = HashtagSerializer(instance)
    obj.save()


@receiver(post_delete, sender=Hashtag, dispatch_uid="delete_hashtag_index")
def delete_es_hashtag_record(sender, instance, *args, **kwargs):
    obj = HashtagSerializer(instance)
    obj.delete(ignore=404)


@receiver(post_save, sender=Product, dispatch_uid="update_product_index")
def update_es_product_record(sender, instance, **kwargs):
    request_ctx = kwargs.get('request_ctx', _get_req_ctx())
    obj = ProductSerializer(instance, context=request_ctx)
    obj.save()
