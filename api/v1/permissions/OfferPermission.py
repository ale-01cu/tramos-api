from rest_framework import permissions, exceptions


class OfferPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list']:
            return True
        user = request.user
        if user is None:
            raise exceptions.NotAuthenticated(detail='User is not authenticated')
        if view.action in ['list', 'retrieve']:
            return user.is_authenticated
        return user.role == 'gestor' or user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        if view.action in ['list']:
            return True
        user = request.user
        if user is None:
            raise exceptions.NotAuthenticated(detail='User is not authenticated')
        if view.action in ['list', 'retrieve']:
            return user.is_authenticated
        return user.role == 'gestor' or user.role == 'admin'
