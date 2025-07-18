from rest_framework import serializers
from api.models.PaymentCode import PaymentCode

class PaymentCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCode
        fields = '__all__'
