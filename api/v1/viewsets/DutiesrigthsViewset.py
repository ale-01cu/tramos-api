from rest_framework import viewsets, mixins

from api.models import Dutiesrigths
from api.v1.serializers import DutiesrigthsSerializer
from api.v1.pagination import PaginationCursorPagination


class DutiesrigthsViewset(viewsets.GenericViewSet,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin):
    queryset = Dutiesrigths.objects.all()
    serializer_class = DutiesrigthsSerializer
    ordering_fields = '__all__'
    pagination_class = PaginationCursorPagination
