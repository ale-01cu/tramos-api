from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.models import Course, Service


class ServiceField(serializers.CharField):

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, value):
        return get_object_or_404(Service, name=value)


class CourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    paymentCOde = serializers.IntegerField(read_only=True)
    rank = serializers.IntegerField(read_only=True)
    service = ServiceField()

    class Meta:
        model = Course
        fields = '__all__'
