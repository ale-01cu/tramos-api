from api.models import ClientClasses
from rest_framework import serializers


class ClientClassesSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ClientClasses
        fields = '__all__'