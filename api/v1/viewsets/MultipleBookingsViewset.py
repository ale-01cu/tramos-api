from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from api.models import Company
from api.v1.permissions import MultipleBookingPermission
from api.v1.serializers import MultipleBookingSerializer
from api.v1.pagination import PaginationCursorPagination


class MultipleBookingsViewset(viewsets.ModelViewSet):
    serializer_class = MultipleBookingSerializer
    permission_classes = [MultipleBookingPermission]
    pagination_class = PaginationCursorPagination
    queryset = MultipleBookingSerializer.Meta.model.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        company = self.request.query_params.get('company')
        if not company:
            raise ValidationError('Company is required')
        company = Company.objects.get(id=company)
        queryset = queryset.filter(company=company)
        return queryset


