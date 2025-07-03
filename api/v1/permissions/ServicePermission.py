from rest_framework import permissions, exceptions


class ServicePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list']:
            return True
        user = request.user
        if not user.is_authenticated:
            raise exceptions.NotAuthenticated(detail='user is None')
        if view.action in ['list', 'create', 'patch', 'delete', 'list', 'retrieve']:
            return user.rol == 'admin'

    def has_object_permission(self, request, view, obj):
        if view.action in ['list']:
            return True
        user = request.user
        if not user.is_authenticated:
            raise exceptions.NotAuthenticated(detail='user is None')
        return user.rol == 'admin'
