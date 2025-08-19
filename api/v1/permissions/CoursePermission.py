from rest_framework import permissions, exceptions


class CoursePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user is None:
            raise exceptions.NotAuthenticated(detail='User is not authenticated')
        if view.action in ['create', 'patch', 'delete', 'update', 'partial_update']:
            return user.role == 'admin' or user.role == 'gestor'

        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['list']:
            return True
        user = request.user
        if user is None:
            raise exceptions.NotAuthenticated(detail='User is None')
        return user.role == 'admin' or user.role == 'gestor'
