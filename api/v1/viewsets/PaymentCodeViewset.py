from rest_framework import viewsets, permissions
from api.v1.serializers import PaymentCodeSerializer
from api.v1.pagination import PaginationCursorPagination


class PaymentCodeViewset(viewsets.ModelViewSet):
    queryset = PaymentCodeSerializer.Meta.model.objects.all()
    serializer_class = PaymentCodeSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = '__all__'
    pagination_class = PaginationCursorPagination
