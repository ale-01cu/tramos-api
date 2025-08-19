from rest_framework import permissions, exceptions


class ServicePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            raise exceptions.NotAuthenticated(detail='user is None')
        return user.role == 'admin' or user.role == 'gestor'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            raise exceptions.NotAuthenticated(detail='user is None')
        return user.role == 'admin' or user.role == 'gestor'
