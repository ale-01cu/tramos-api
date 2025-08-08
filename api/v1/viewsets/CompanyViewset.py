from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action

from api.models import Company, MultipleBooking
from api.v1.permissions.CompanyPermission import CompanyPermission
from api.v1.serializers.CompanySerializer import CompanySerializer
from api.v1.serializers.LoginCompanySerializer import LoginCompanySerializer
from api.v1.pagination import PaginationCursorPagination


class CompanyViewset(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, CompanyPermission]
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['name', 'description', 'contract']
    pagination_class = PaginationCursorPagination

    @action(detail=False, methods=['POST'], serializer_class=LoginCompanySerializer)
    def login_company(self, request):
        serializer = LoginCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contract = serializer.validated_data['contract']
        company_name = serializer.validated_data['name']
        verify = get_object_or_404(Company, contract=contract, name__contains=company_name)
        company_bookings = MultipleBooking.objects.filter(company=verify)
        return Response(company_bookings, status=status.HTTP_200_OK)
