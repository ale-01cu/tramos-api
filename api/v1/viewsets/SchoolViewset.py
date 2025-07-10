from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from api.models import School
from api.v1.filters import SchoolFilter
from api.v1.serializers import SchoolSerializer, SchoolCreateSerializer


class SchoolViewset(viewsets.ModelViewSet):
    queryset = School.objects.all()
    # serializer_class = SchoolSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SchoolFilter

    def get_serializer_class(self):
        """
        Determina qué serializador usar basado en la acción.
        """
        # self.action contendrá 'list', 'create', 'retrieve', 'update', 'partial_update'
        if self.action in ['create', 'update', 'partial_update']:
            return SchoolCreateSerializer  # Usa este para escribir datos

        # Para cualquier otra acción ('list', 'retrieve', etc.), usa el serializador por defecto.
        return SchoolSerializer  # Usa este para leer datos
