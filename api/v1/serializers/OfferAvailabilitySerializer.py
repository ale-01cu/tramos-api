from rest_framework import serializers

from api.models import OfferAvailability


class OfferAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferAvailability
        fields = ('offer', 'time', 'availability', 'group_code')


class OfferAvailabilityCreateWithOfferSerializer(serializers.ModelSerializer):
    # time = serializers.CharField(required=True)

    class Meta:
        model = OfferAvailability
        fields = ('time', 'availability', 'group_code')
