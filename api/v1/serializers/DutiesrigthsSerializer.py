from rest_framework import serializers

from api.models import Dutiesrigths


class DutiesrigthsSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Dutiesrigths
        fields = '__all__'
