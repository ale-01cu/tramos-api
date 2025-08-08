from rest_framework import serializers

from api.models import Dutiesrigths


class DutiesrigthsSerializer(serializers.ModelSerializer):
    description = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Dutiesrigths
        fields = '__all__'
