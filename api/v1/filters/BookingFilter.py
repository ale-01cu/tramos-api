import django_filters
from api.models import Booking, Client, Offer, Classroom
from django.db import models


class BookingFilter(django_filters.FilterSet):
    # Filtros existentes...
    client = django_filters.ModelChoiceFilter(queryset=Client.objects.all())
    offer = django_filters.ModelChoiceFilter(queryset=Offer.objects.all())
    classroom = django_filters.ModelChoiceFilter(queryset=Classroom.objects.all())
    start_date = django_filters.DateFilter(field_name='registeredDate', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='registeredDate', lookup_expr='lte')
    client_name = django_filters.CharFilter(field_name='client__name', lookup_expr='icontains')

    # Nuevo filtro para expiración
    is_expired = django_filters.BooleanFilter(method='filter_expired')

    def filter_expired(self, queryset, name, value):
        """
        Filtra por reservas expiradas (True) o no expiradas (False)
        """
        from django.utils import timezone
        now = timezone.now()

        if value:  # True = mostrar solo expiradas
            return queryset.filter(
                isPaid=False,
                expirationDate__lte=now
            )
        else:  # False = mostrar solo no expiradas
            return queryset.filter(
                models.Q(isPaid=True) |
                (models.Q(isPaid=False) & models.Q(expirationDate__gt=now))
            )

    class Meta:
        model = Booking
        fields = ['client', 'offer', 'classroom', 'isPaid', 'typePayment', 'start_date', 'end_date', 'client_name',
                  'is_expired']