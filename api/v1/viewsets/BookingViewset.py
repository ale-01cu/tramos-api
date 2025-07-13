from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters

from api.models import Booking
from api.v1.serializers import BookingSerializer, BookingCreateSerializer
from api.v1.filters.BookingFilter import BookingFilter


class BookingViewset(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    # filterset_fields = ['name', 'school']
    # En lugar de filterset_fields, ahora usas filterset_class
    filterset_class = BookingFilter

    def get_serializer_class(self):
        """
        Determina qué serializador usar basado en la acción.
        """
        # self.action contendrá 'list', 'create', 'retrieve', 'update', 'partial_update'
        if self.action in ['create', 'update', 'partial_update']:
            return BookingCreateSerializer  # Usa este para escribir datos

        # Para cualquier otra acción ('list', 'retrieve', etc.), usa el serializador por defecto.
        return BookingSerializer  # Usa este para leer datos

