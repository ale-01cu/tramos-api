from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, permissions
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Client, Booking
from api.v1.filters import ClientFilter
from api.v1.serializers import ClientSerializer, BookingSerializer, ChangeCodeSerializer, PaginatedBookingSerializer
from api.v1.permissions.ClientPermission import ClientPermission
from api.v1.pagination import PaginationCursorPagination
from django.shortcuts import get_object_or_404

class ClientViewset(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated, ClientPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientFilter
    pagination_class = PaginationCursorPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Client.objects.all()
        search = self.request.query_params.get('search', None)
        if user.is_authenticated and user.role == 'admin' and search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(last_name__icontains=search) | Q(ci__icontains=search))
        return queryset

    @action(detail=True, methods=["patch"], serializer_class=ChangeCodeSerializer)
    def change_code(self, request, pk=None):
        user = request.user
        client = Client.objects.get(pk=pk)
        new_code: str = request.data.get('code')
        if not (user.is_authenticated and user.role == 'admin'):
            raise Exception('Unauthorized', status.HTTP_401_UNAUTHORIZED)
        client.code = new_code
        client.save()
        return Response({'detail': 'Code changed'}, status=status.HTTP_200_OK)


    @action(detail=True, methods=["get"], serializer_class=PaginatedBookingSerializer)
    def bookings(self, request, pk=None):
        client = get_object_or_404(Client, id=pk)

        bookings = Booking.objects.filter(
            client=client,
            expirationDate__gte=datetime.now()
        )

        # Aplicar paginación
        paginator = self.paginator  # Usa el paginator definido en tu ViewSet
        paginated_bookings = paginator.paginate_queryset(bookings, request)

        # Serializar los datos paginados
        serializer = BookingSerializer(paginated_bookings, many=True)

        # Devolver respuesta paginada
        return paginator.get_paginated_response(serializer.data)

