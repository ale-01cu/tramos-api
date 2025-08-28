from rest_framework import permissions, exceptions

class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role == 'admin'