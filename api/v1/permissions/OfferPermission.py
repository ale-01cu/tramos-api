from rest_framework import permissions, exceptions


class OfferPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        user = request.user
        if user is None:
            raise exceptions.NotAuthenticated(detail='User is not authenticated')

        return user.role == 'gestor' or user.role == 'admin' or user.role == 'comercial' or user.role == 'cajero'

    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'retrieve']:
            return True
        user = request.user
        if user is None:
            raise exceptions.NotAuthenticated(detail='User is not authenticated')

        return user.role == 'gestor' or user.role == 'admin' or user.role == 'comercial' or user.role == 'cajero'
