import django_filters
from django_filters import FilterSet

from api.models import School


class SchoolFilter(FilterSet):

    class Meta:
        model = School
        fields = ['name']
