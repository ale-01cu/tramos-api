# serializers.py
from rest_framework import serializers

class PaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    phone_number = serializers.CharField(max_length=20)
    external_id = serializers.CharField(max_length=50)



class TransfermovilCallbackSerializer(serializers.Serializer):
    ExternalId = serializers.CharField(required=True)