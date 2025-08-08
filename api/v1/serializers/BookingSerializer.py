from rest_framework import serializers
from django.utils import timezone

from api.models import Booking, Client, OfferAvailability
from api.v1.serializers.ClientSerializer import ClientRelatedField


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class BookingCreateSerializer(serializers.ModelSerializer):
    client = ClientRelatedField(queryset=Client.objects.all())
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Booking
        fields = ('client', 'offer', 'typePayment',
                  'offerAvailability', 'created_at')
        read_only_fields = ('expirationDate', 'registeredDate', 'created_at')

    def validate(self, data):
        offer = data.get('offer')
        offer_availability = data.get('offerAvailability')
        client_input = data.get('client')

        client_instance = None
        client_ci = None

        # Determinamos si el cliente ya existe o es nuevo
        if isinstance(client_input, Client):  # Caso 1: Se pasó un ID, client_input es una instancia de Client
            client_instance = client_input
            client_ci = client_instance.ci
        elif isinstance(client_input, dict):  # Caso 2: Se pasaron datos, client_input es un diccionario
            client_ci = client_input.get('ci')
            # Verificamos si un cliente con ese CI ya existe en la BD
            if client_ci:
                client_instance = Client.objects.filter(ci=client_ci).first()

        # Validar que la oferta no haya expirado
        if offer.date_end_offer < timezone.now():
            raise serializers.ValidationError({'offer': 'La oferta ha expirado.'})

        # Validar que el cliente no tenga ya una reserva para esta oferta
        if client_instance and Booking.objects.filter(client=client_instance, offer=offer).exists():
            raise serializers.ValidationError(
                {'client': 'Este cliente ya tiene una reserva para esta oferta.'})

        # Validar disponibilidad
        try:
            if offer_availability.availability <= 0:
                raise serializers.ValidationError(
                    {'offer': 'No hay cupos disponibles para esta oferta en el horario seleccionado.'})
        except OfferAvailability.DoesNotExist:
            raise serializers.ValidationError(
                {'offerAvailability': 'No hay disponibilidad para la fecha y hora seleccionada.'})

        return data

    def create(self, validated_data):
        client_input = validated_data.pop('client')
        offer = validated_data.get('offer')
        offer_availability = validated_data.get('offerAvailability')
        client_instance = None

        # --- Lógica principal para manejar los dos casos de cliente ---
        if isinstance(client_input, Client):
            # Caso 1: El cliente ya existía y se pasó por ID.
            client_instance = client_input
        elif isinstance(client_input, dict):
            # Caso 2: Se pasaron los datos de un cliente. Usamos get_or_create.
            client_data = client_input
            client_instance, created = Client.objects.get_or_create(
                ci=client_data.get('ci'),
                defaults=client_data
            )
            if not created:
                # Si el cliente ya existía, actualizamos sus datos por si han cambiado.
                for attr, value in client_data.items():
                    setattr(client_instance, attr, value)
                client_instance.save()

        # Si por alguna razón no tenemos una instancia de cliente, lanzamos un error.
        if not client_instance:
            raise serializers.ValidationError("No se pudo determinar el cliente para la reserva.")

        # Creamos la reserva
        booking_instance = Booking.objects.create(client=client_instance, **validated_data)

        # Decrementamos la disponibilidad (envuelto en un bloque try-except para seguridad)
        try:
            availability_slot = OfferAvailability.objects.filter(offer=offer, time=offer_availability.time).first()
            availability_slot.availability -= 1
            availability_slot.save()
        except OfferAvailability.DoesNotExist:
            # Aunque esto se valida en `validate`, es una buena práctica manejarlo aquí también
            # en caso de una condición de carrera (race condition).
            # Aquí podrías decidir si eliminar la reserva recién creada o marcarla como inválida.
            booking_instance.delete()
            raise serializers.ValidationError(
                {'offerAvailability': 'La disponibilidad cambió. Inténtelo de nuevo.'})

        return booking_instance