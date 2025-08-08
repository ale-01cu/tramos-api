from rest_framework import serializers

from api.models import ActionTraces


class ActionTracesSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ActionTraces
        fields = '__all__'
        