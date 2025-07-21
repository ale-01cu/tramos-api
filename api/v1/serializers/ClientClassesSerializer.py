from api.models import ClientClasses
from rest_framework import serializers


class ClientClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientClasses
        fields = '__all__'