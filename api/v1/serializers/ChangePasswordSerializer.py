from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)


