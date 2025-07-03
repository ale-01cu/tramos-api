from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from api.models import MultipleBooking
from api.v1.permissions import MultipleBookingPermission
from api.v1.serializers import MultipleBookingSerializer


class MultipleBookingsViewset(viewsets.ModelViewSet):
    model = MultipleBooking
    serializer_class = MultipleBookingSerializer
    permission_classes = [MultipleBookingPermission]

    def get_queryset(self):
        queryset = self.queryset
        company = self.request.query_params.get('company')
        if not company:
            raise ValidationError('Company is required')
        queryset = queryset.filter(company=company)
        return queryset


