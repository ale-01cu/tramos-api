from rest_framework import permissions, exceptions


class ClassroomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        user = request.user
        if user is None:
            raise exceptions.NotAuthenticated(detail='User is None')

        if view.action in ['create', 'patch', 'delete']:
            return user.role == 'admin' or user.role == 'gestor'




