from rest_framework import serializers

from api.models import Booking, Client
from api.v1.serializers import ClientSerializer

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'



class BookingCreateSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    class Meta:
        model = Booking
        fields = ('client', 'offer', 'typePayment',
                  'scheduleOfferDate')


    def create(self, validated_data):
        client_data = validated_data.pop('client')
        ci = client_data.get('ci')
        if Client.objects.filter(ci=ci).exists():
            raise serializers.ValidationError({'client': 'Ya existe un cliente con este CI.'})
        client_instance = Client.objects.create(**client_data)
        booking_instance = Booking.objects.create(client=client_instance, **validated_data)
        return booking_instance