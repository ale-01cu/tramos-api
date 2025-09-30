from rest_framework import serializers
from django.utils import timezone

from api.models import Booking, Client
from api.v1.serializers.ClientSerializer import ClientRelatedField


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class BookingCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Booking
        fields = ('client', 'offer', 'typePayment',
                  'created_at')
        read_only_fields = ('expirationDate', 'created_at')

    def validate(self, data):
        offer = data.get('offer')
        # offer_availability = data.get('offerAvailability')
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


        bookings_count = Booking.objects.filter(offer=offer).count()
        capacity = offer.classroom.capacity

        if bookings_count >= capacity:
            raise serializers.ValidationError(
                {'offer': 'No hay cupos disponibles para esta oferta en el horario seleccionado.'})


        # Validar capacidad del aula
        if offer.classroom:
            classroom = offer.classroom
            # Check if classroom can accommodate one more booking
            if not classroom.can_accommodate(1):
                current_bookings = classroom.get_current_bookings()
                raise serializers.ValidationError({
                    'offer': f'El aula "{classroom.name}" está llena. '
                             f'Capacidad máxima: {classroom.capacity}, '
                             f'Reservas actuales: {current_bookings}'
                })

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
        return booking_instance


class PaginatedBookingSerializer(serializers.Serializer):
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    results = BookingSerializer(many=True)