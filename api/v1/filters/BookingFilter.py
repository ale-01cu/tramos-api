import django_filters
from api.models import Booking, Client, Offer, Classroom

class BookingFilter(django_filters.FilterSet):
    # Filtro por el ID del cliente (igual que el método simple)
    client = django_filters.ModelChoiceFilter(queryset=Client.objects.all())

    # Filtro por el ID de la oferta
    offer = django_filters.ModelChoiceFilter(queryset=Offer.objects.all())

    # Filtro por el ID del aula
    classroom = django_filters.ModelChoiceFilter(queryset=Classroom.objects.all())

    # Ejemplo de un filtro más complejo: por rango de fechas de registro
    start_date = django_filters.DateFilter(field_name='registeredDate', lookup_expr='gte')  # mayor o igual que
    end_date = django_filters.DateFilter(field_name='registeredDate', lookup_expr='lte')  # menor o igual que

    # Ejemplo para filtrar por el nombre del cliente (atravesando la relación)
    client_name = django_filters.CharFilter(field_name='client__name', lookup_expr='icontains')

    class Meta:
        model = Booking
        # Aquí defines los campos que quieres que se filtren de forma exacta y automática
        # además de los que definiste manualmente arriba.
        fields = ['client', 'offer', 'classroom', 'isPaid', 'typePayment', 'start_date', 'end_date', 'client_name']