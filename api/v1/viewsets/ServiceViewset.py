from rest_framework import viewsets, permissions

from api.models import Service
from api.v1.permissions import ServicePermission
from api.v1.serializers import ServiceSerializer


class ServiceViewset(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, ServicePermission]
    ordering_fields = '__all__'

