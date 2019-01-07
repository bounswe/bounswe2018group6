"""
.. module:: permission
   :platform: Unix, Windows
   :synopsis: Permission

"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class IsOwnerOrParticipant(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or obj.participant == request.user