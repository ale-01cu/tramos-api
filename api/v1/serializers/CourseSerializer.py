from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.models import Course, Service
from api.v1.serializers.PaymentCodeSerializer import PaymentCodeSerializer
from api.models.PaymentCode import PaymentCode

class ServiceField(serializers.CharField):

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, value):
        return get_object_or_404(Service, name=value)


class CourseSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(read_only=True)
    # description = serializers.CharField(read_only=True)
    paymentCOde = serializers.IntegerField(read_only=True)
    rank = serializers.IntegerField(read_only=True)
    paymentCode = serializers.PrimaryKeyRelatedField(queryset=PaymentCode.objects.all())
    # service = ServiceField()

    class Meta:
        model = Course
        fields = '__all__'


    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Si el campo existe y está presente, reemplazamos el ID por el JSON completo
        if hasattr(instance, 'paymentCode') and instance.paymentCode:
            data['paymentCode'] = PaymentCodeSerializer(instance.paymentCode).data
        return data
