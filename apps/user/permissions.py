#!/usr/bin/env python
# coding=utf-8
from rest_framework import permissions
from rest_framework.permissions import BasePermission


class SelfOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, user):
        return request.method in permissions.SAFE_METHODS or user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.owner == request.user
