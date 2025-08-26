from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from api.models import Company
from api.v1.permissions import MultipleBookingPermission
from api.v1.serializers import MultipleBookingSerializer
from api.v1.pagination import PaginationCursorPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter

def company_query_param():
    """Decorador reutilizable para el parámetro company"""
    return extend_schema(
        parameters=[
            OpenApiParameter(
                'company',
                int,
                description='ID de la compañía (requerido)',
                required=True
            )
        ]
    )

class MultipleBookingsViewset(viewsets.ModelViewSet):
    serializer_class = MultipleBookingSerializer
    permission_classes = [MultipleBookingPermission]
    pagination_class = PaginationCursorPagination
    queryset = MultipleBookingSerializer.Meta.model.objects.all()

    @company_query_param()
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @company_query_param()
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @company_query_param()
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @company_query_param()
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


    def get_queryset(self):
        queryset = self.queryset
        company = self.request.query_params.get('company')
        if not company:
            raise ValidationError('Company is required')
        company = Company.objects.get(id=company)
        queryset = queryset.filter(company=company)
        return queryset


