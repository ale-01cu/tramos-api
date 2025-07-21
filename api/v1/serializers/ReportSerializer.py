from rest_framework import serializers
from api.models import ClientClasses, Offer, OfferAvailability, Booking


# Serializer para la lista de clientes/estudiantes en el reporte
class ReportClientSerializer(serializers.ModelSerializer):
    clientCI = serializers.CharField(source='client.ci')
    clientName = serializers.CharField(source='client.name')
    clientLastName = serializers.CharField(source='client.last_name')

    # Este campo es un buen candidato para un SerializerMethodField
    # ya que no está directamente en el modelo ClientClasses.
    contractCompany = serializers.SerializerMethodField()

    class Meta:
        model = ClientClasses
        fields = [
            'id',
            'offer_id',  # Asumiendo que quieres el ID de la oferta
            'scheduleOfferDate',
            'client_id',  # Y el ID del cliente
            'clientCI',
            'clientName',
            'clientLastName',
            'evaluationConfirmed',
            'is_graduated',
            'graduatedDate',
            'bookingCode',
            'contractCompany',
        ]

    def get_contractCompany(self, obj: ClientClasses):
        # Lógica para obtener la compañía del contrato.
        # Asumimos que si la oferta está asociada a una compañía, esa es la del contrato.
        if obj.offer.company:
            return obj.offer.company.name
        return ""


# Serializer para el horario dentro de los detalles de la oferta
class ReportOfferAvailabilitySerializer(serializers.ModelSerializer):
    # Formateamos el tiempo para que coincida con el ejemplo "01:00 p. m."
    dateTime = serializers.TimeField(source='time', format='%I:%M %p')
    availabilityCount = serializers.IntegerField(source='availability')

    class Meta:
        model = OfferAvailability
        fields = ['dateTime', 'availabilityCount', 'group_code']


# Serializer para el objeto de detalles de la oferta
class ReportOfferDetailSerializer(serializers.ModelSerializer):
    # Renombramos y obtenemos campos de modelos relacionados
    planId = serializers.IntegerField(source='course.id')
    priceToPay = serializers.DecimalField(source='course.priceToPay', max_digits=10, decimal_places=2)
    classroomId = serializers.IntegerField(source='classroom.id')
    classroomDisplayName = serializers.CharField(source='classroom.name')
    classroomDisplayAddress = serializers.CharField(source='classroom.address')
    schoolDisplayName = serializers.CharField(source='classroom.school.name')
    schoolDisplayAddress = serializers.CharField(source='classroom.school.address')
    dateStart = serializers.DateTimeField(source='date_start_course')
    dateFinish = serializers.DateTimeField(source='date_end_course')
    planDisplayName = serializers.CharField(source='course.name')

    # Usamos el serializer anidado para la lista de horarios
    scheduleOffer = ReportOfferAvailabilitySerializer(source='offeravailability_set', many=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'planId',
            'priceToPay',
            'classroomId',
            'classroomDisplayName',
            'classroomDisplayAddress',
            'schoolDisplayName',
            'schoolDisplayAddress',
            'description',
            'dateStart',
            'dateFinish',
            'date_start_offer',
            'date_end_offer',
            'scheduleOffer',
            'planDisplayName'
        ]


# Serializer para la lista de bookings en el reporte "COMPARECENCIA TODO"
class ReportBookingSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name')
    client_last_name = serializers.CharField(source='client.last_name')
    client_ci = serializers.CharField(source='client.ci')

    class Meta:
        model = Booking
        fields = [
            'id',
            'client_name',
            'client_last_name',
            'client_ci',
            'isPaid',
            'paidDate',
            'typePayment',
            'transactionCode'
        ]