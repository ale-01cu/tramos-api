from rest_framework import serializers


class LoginCompanySerializer(serializers.Serializer):
    contract = serializers.CharField(required=True)
    name = serializers.CharField(required=True)