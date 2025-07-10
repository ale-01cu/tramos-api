from rest_framework import serializers

from api.models import Municipality
from .ProvinceSerializer import ProvinceSerializer


class MunicipalitySerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()

    class Meta:
        model = Municipality
        fields = '__all__'

class MunicipalityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = '__all__'
