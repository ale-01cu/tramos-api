from rest_framework import serializers
from api.models import Province


class ProvinceSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Province
        fields = '__all__'
