from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, generics

from api.models import Municipality
from api.v1.serializers import MunicipalitySerializer, MunicipalityCreateSerializer
from api.v1.pagination import PaginationCursorPagination


class MunicipalityViewset(viewsets.ModelViewSet):
    queryset = Municipality.objects.all()
    # serializer_class ya no se define aquí, o se usa como default
    ordering_fields = '__all__'
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['province__name']
    pagination_class = PaginationCursorPagination

    def get_serializer_class(self):
        """
        Determina qué serializador usar basado en la acción.
        """
        # self.action contendrá 'list', 'create', 'retrieve', 'update', 'partial_update'
        if self.action in ['create', 'update', 'partial_update']:
            return MunicipalityCreateSerializer  # Usa este para escribir datos

        # Para cualquier otra acción ('list', 'retrieve', etc.), usa el serializador por defecto.
        return MunicipalitySerializer  # Usa este para leer datos
