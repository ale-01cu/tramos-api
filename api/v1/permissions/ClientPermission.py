from rest_framework import permissions, exceptions

class ClientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user is None:
            raise exceptions.NotAuthenticated(detail='User is None')

        return user.role == 'admin' or user.role == 'gestor' or user.role == 'comercial' or user.role == 'cajero'




