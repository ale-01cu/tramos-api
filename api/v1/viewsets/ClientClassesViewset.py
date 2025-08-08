from rest_framework import viewsets, permissions
from api.v1.serializers import ClientClassesSerializer
from api.v1.permissions.ClientClassesPermission import ClientClassesPermission
from api.v1.pagination import PaginationCursorPagination


class ClientClassesViewset(viewsets.ModelViewSet):
    queryset = ClientClassesSerializer.Meta.model.objects.all()
    serializer_class = ClientClassesSerializer
    permission_classes = [permissions.IsAuthenticated, ClientClassesPermission]
    pagination_class = PaginationCursorPagination