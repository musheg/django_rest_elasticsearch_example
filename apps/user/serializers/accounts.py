from rest_framework import serializers
from rest_framework_elasticsearch.es_serializer import ElasticModelSerializer

from apps.user.models import User
from apps.user.search_indexes import UserIndex


class UserSerializer(ElasticModelSerializer):
    email_verified = serializers.SerializerMethodField()
    can_charge = serializers.ReadOnlyField(source='customer.can_charge')

    class Meta:
        es_model = UserIndex
        model = User
        fields = [
            'id',
            'full_name',
            'username',
            'email',
            'age',
            'gender',
            'photo',
            'email_verified',
            'can_charge',
        ]

        read_only_fields = [
            'username'
        ]

    def get_email_verified(self, instance):
        try:
            return instance.emailaddress_set.get(email=instance.email).verified
        except Exception:
            return False


class PublicUserSerializer(ElasticModelSerializer):
    following = serializers.BooleanField(read_only=True, source='is_followed', required=False)

    class Meta:
        model = User
        es_model = UserIndex
        fields = [
            'id',
            'full_name',
            'photo',
            'username',
            'url',
            'following'
        ]

        read_only_fields = [
            'username'
        ]
