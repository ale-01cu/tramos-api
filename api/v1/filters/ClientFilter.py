from django_filters import FilterSet

from api.models import Client


class ClientFilter(FilterSet):

    class Meta:
        model = Client
        fields = ['ci']
