from rest_framework import permissions, exceptions

class ClientClassesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user is None:
            raise exceptions.NotAuthenticated(detail='User is None')

        if view.action in ['list', 'retrieve', 'create', 'patch', 'delete']:
            return user.role == 'admin'




