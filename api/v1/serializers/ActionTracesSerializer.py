from rest_framework import serializers

from api.models import ActionTraces


class ActionTracesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActionTraces
        fields = '__all__'
        