from rest_framework import serializers

from api.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Service
        fields = '__all__'
