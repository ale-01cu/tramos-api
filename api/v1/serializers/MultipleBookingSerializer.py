from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import MultipleBooking, Company


class CompanyField(serializers.CharField):

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, value):
        return get_object_or_404(Company, name=value)


class MultipleBookingSerializer(serializers.ModelSerializer):
    # company = CompanyField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = MultipleBooking
        fields = '__all__'


    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Si el campo existe y está presente, reemplazamos el ID por el JSON completo
        if hasattr(instance, 'company') and instance.company:
            data['company'] = instance.company.name
        return data
