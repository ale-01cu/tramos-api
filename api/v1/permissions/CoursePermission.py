from rest_framework import permissions, exceptions


class CoursePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list']:
            return True
        user = request.user
        if user is None:
            raise exceptions.NotAuthenticated(detail='User is not authenticated')
        if view.action in ['list', 'create', 'patch', 'delete', 'retrieve']:
            return user.role == 'admin' or user.role == 'gestor'

    def has_object_permission(self, request, view, obj):
        if view.action in ['list']:
            return True
        user = request.user
        if user is None:
            raise exceptions.NotAuthenticated(detail='User is None')
        return user.role == 'admin' or user.role == 'gestor'
