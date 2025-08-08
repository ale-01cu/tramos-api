from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.models import School, Municipality
from api.v1.serializers.PaymentCodeSerializer import PaymentCodeSerializer
from api.models.PaymentCode import PaymentCode

class MunicipalityField(serializers.CharField):

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, value):
        return get_object_or_404(Municipality, name=value)


class SchoolSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=200)
    providerNumber = serializers.IntegerField()
    paymentCode = PaymentCodeSerializer(read_only=True)
    municipality = MunicipalityField()
    province = serializers.CharField(source='municipality.province.name', read_only=True)

    class Meta:
        model = School
        fields = '__all__'

class SchoolCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=200)
    providerNumber = serializers.IntegerField()
    # municipality = serializers.SerializerMethodField(read_only=True)
    municipality = MunicipalityField(read_only=True)
    municipality_id = serializers.PrimaryKeyRelatedField(
        queryset=Municipality.objects.all(),
        source='municipality',  # Mapea al campo del modelo
        write_only=True  # Solo para escritura, no aparece en respuestas
    )
    paymentCode = serializers.PrimaryKeyRelatedField(queryset=PaymentCode.objects.all())
    province = serializers.CharField(source='municipality.province.name', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = School
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Si el campo existe y está presente, reemplazamos el ID por el JSON completo
        if hasattr(instance, 'paymentCode') and instance.paymentCode:
            data['paymentCode'] = PaymentCodeSerializer(instance.paymentCode).data
        return data



