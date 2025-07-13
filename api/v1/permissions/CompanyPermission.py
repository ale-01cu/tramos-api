from rest_framework import permissions, exceptions


class CompanyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['login_company']:
            return True
        user = request.user
        if user is None:
            raise exceptions.NotAuthenticated(detail='User is None')
        if view.action in ['create', 'patch', 'delete', 'list', 'retrieve']:
            return user.is_authenticated

        return user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if view.action in ['login_company']:
            return True
        if user is None:
            raise exceptions.NotAuthenticated(detail='user is None')
        return user.role == 'admin'




