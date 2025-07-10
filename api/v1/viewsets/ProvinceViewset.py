from rest_framework import viewsets, permissions

from api.models import Province
from api.v1.serializers import ProvinceSerializer


class ProvinceViewset(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = '__all__'
