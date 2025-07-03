from rest_framework import serializers

from api.models import Client


class ClientSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    ci = serializers.CharField()
    sex = serializers.BooleanField()

    class Meta:
        model = Client
        fields = ['id', 'name', 'last_name', 'phone_number', 'email', 'sex', 'ci']
        read_only_fields = ['code']
