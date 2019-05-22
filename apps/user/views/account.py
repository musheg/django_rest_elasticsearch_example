#!/usr/bin/env python
# coding=utf-8

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.user.models import User
from apps.user.permissions import SelfOrReadOnly
from apps.user.serializers.accounts import UserSerializer, PublicUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    # /users/me/ refers to the current user
    SELF_LOOKUP_VALUE = 'me'

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, SelfOrReadOnly)

    def initialize_request(self, request, *args, **kwargs):
        """
        'Rewrite' /users/me/ urls to /users/x/ where x is the user id of the current logged in user. We can't do it
        in dispatch, unfortunately, where it would make the most sense, because authentication happens only after we
        call the inherited dispatch method.
        """
        drf_request = super().initialize_request(request, *args, **kwargs)

        if self.lookup_field in self.kwargs and self.kwargs[self.lookup_field] == self.SELF_LOOKUP_VALUE:
            self.kwargs[self.lookup_field] = str(drf_request.user.id)

        return drf_request

    @detail_route(methods=['GET'])
    def following(self, request, pk=None):
        user = self.get_object()
        return Response(PublicUserSerializer(user.following.all(), many=True, context={'request': request}).data)

    @detail_route(methods=['GET', 'POST', 'DELETE'], permission_classes=(IsAuthenticated,))
    def followers(self, request, pk=None):
        user = self.get_object()
        current_user = self.request.user

        if request.method == 'POST':
            if user != current_user:
                self.get_object().add_follower(current_user)
                return Response(status=status.HTTP_201_CREATED, data={})

            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': "You can't follow yourself."})
        elif request.method == 'DELETE':
            self.get_object().remove_follower(current_user)
            return Response(status=status.HTTP_200_OK, data={})

        return Response(PublicUserSerializer(user.followers.all(), many=True, context={'request': request}).data)

    def get_serializer_class(self):
        return self.serializer_class if self.get_object() == self.request.user else PublicUserSerializer


class FollowerView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.followers.all()


class FollowingView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.following.all()
