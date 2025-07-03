from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.models import School, Municipality


class MunicipalityField(serializers.CharField):

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, value):
        return get_object_or_404(Municipality, name=value)


class SchoolSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=200)
    providerNumber = serializers.IntegerField()
    paymentCode = serializers.CharField()
    municipality = MunicipalityField()
    province = serializers.CharField(source='municipality.province.name', read_only=True)

    class Meta:
        model = School
        fields = '__all__'

