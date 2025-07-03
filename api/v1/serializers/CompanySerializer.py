from rest_framework import serializers

from api.models import Company


class CompanySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    contract = serializers.CharField()
    description = serializers.CharField()
    dateContractStart = serializers.DateField()
    dateContractFinish = serializers.DateField()

    class Meta:
        model = Company
        fields = '__all__'
