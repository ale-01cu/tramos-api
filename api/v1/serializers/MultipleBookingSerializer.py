from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import MultipleBooking, Company


class CompanyField(serializers.CharField):

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, value):
        return get_object_or_404(Company, name=value)


class MultipleBookingSerializer(serializers.ModelSerializer):
    company = CompanyField()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = MultipleBooking
        fields = '__all__'
