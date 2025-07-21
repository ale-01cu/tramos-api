from rest_framework import serializers

from api.models import Company


class CompanySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        model = Company
        fields = '__all__'
