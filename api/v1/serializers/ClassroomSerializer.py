from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.models import Classroom, Municipality


class MunicipalityField(serializers.CharField):

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, value):
        return get_object_or_404(Municipality, name=value)


class ClassroomSerializer(serializers.ModelSerializer):
    # name = serializers.CharField()
    # description = serializers.CharField()
    # capacity = serializers.IntegerField()
    # is_available = serializers.BooleanField()
    # address = serializers.CharField()
    # province = serializers.CharField(source='municipality.province.name', required=False)
    # municipality = MunicipalityField()
    created_at = serializers.DateTimeField(read_only=True)


    class Meta:
        model = Classroom
        fields = '__all__'
