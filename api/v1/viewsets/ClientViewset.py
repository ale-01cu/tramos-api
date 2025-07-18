from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, permissions
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Client, Booking
from api.v1.filters import ClientFilter
from api.v1.serializers import ClientSerializer
from api.v1.permissions.ClientPermission import ClientPermission

class ClientViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated, ClientPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Client.objects.all()
        search = self.request.query_params.get('search', None)
        if user.is_authenticated and user.role == 'admin' and search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(last_name__icontains=search) | Q(ci__icontains=search))
        return queryset

    @action(detail=True, methods=["patch"])
    def change_code(self, request):
        user = request.user
        client = Client.objects.get(pk=request.data['id'])
        new_code: str = request.query_params.get['code']
        if not (user.is_authenticated and user.role == 'admin'):
            raise Exception('Unauthorized', status.HTTP_401_UNAUTHORIZED)
        if len(new_code) != 4:
            raise Exception('Invalid code')
        client.code = new_code
        client.save()
        return Response({'detail': 'Code changed'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def bookings(self, request):
        ci = request.query_params.get('ci')
        code = request.query_params.get('code')
        client = Client.objects.get(ci=ci)
        if client.code != code:
            raise Exception('Invalid client', status.HTTP_401_UNAUTHORIZED)
        bookings = Booking.objects.filter(client__ci=ci)
        bookings = bookings.objects.filter(expirationDate__gte=datetime.now())
        return Response(bookings, status=status.HTTP_200_OK)

