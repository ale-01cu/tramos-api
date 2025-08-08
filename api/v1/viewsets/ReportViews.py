# en tu archivo views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from api.models import Offer, ClientClasses, Booking, OfferAvailability
# Importa los nuevos serializers que acabamos de crear
from api.v1.serializers import (
    ReportClientSerializer,
    ReportOfferDetailSerializer,
    ReportBookingSerializer
)

REPORT_TYPES = ['asistencia', 'comparecencia', 'comparecencia_todo', 'hoja_de_registro']


@extend_schema(
    summary="Genera reportes de asistencia y evaluación para un curso/oferta.",
    description="""
    Este endpoint genera diferentes tipos de reportes basados en los parámetros proporcionados.

    **Tipos de Reporte (`report_type`):**
    - `asistencia`: Lista de clientes y detalles completos de la oferta.
    - `comparecencia`: Igual que 'asistencia'.
    - `hoja_de_registro`: Igual que 'asistencia'.
    - `comparecencia_todo`: Lista de clientes y una lista detallada de todas las reservas (bookings) para esa oferta.
    """,
    parameters=[
        OpenApiParameter(
            name='report_type',
            description='El tipo de reporte a generar.',
            required=True,
            type=OpenApiTypes.STR,
            enum=REPORT_TYPES
        ),
        OpenApiParameter(
            name='offer_id',
            description='El ID de la Oferta para la cual generar el reporte.',
            required=True,
            type=OpenApiTypes.INT
        ),
        OpenApiParameter(
            name='offer_availability_id',
            description='(Opcional) El ID del Horario (OfferAvailability) específico para filtrar los clientes.',
            required=False,
            type=OpenApiTypes.INT
        )
    ]
)
class CourseReportView(APIView):


    def get(self, request, *args, **kwargs):
        # 1. Obtener y validar parámetros de la URL
        report_type = request.query_params.get('report_type')
        offer_id = request.query_params.get('offer_id')
        offer_availability_id = request.query_params.get('offer_availability_id')

        if not report_type or not offer_id:
            return Response(
                {"error": "Los parámetros 'report_type' y 'offer_id' son obligatorios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if report_type not in REPORT_TYPES:
            return Response(
                {"error": f"El valor de 'report_type' es inválido. Use uno de: {', '.join(REPORT_TYPES)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Obtener el objeto Offer principal
        try:
            offer = Offer.objects.select_related(
                'course', 'classroom__school'
            ).prefetch_related(
                'offeravailability_set'
            ).get(id=offer_id)
        except Offer.DoesNotExist:
            return Response({"error": "La oferta con el ID proporcionado no existe."}, status=status.HTTP_404_NOT_FOUND)

        # 3. Obtener la lista de clientes/estudiantes base
        client_list_qs = ClientClasses.objects.filter(offer=offer).select_related('client', 'offer__company')

        # OJO: Esta parte es una suposición basada en tus modelos.
        # El modelo ClientClasses tiene `scheduleOfferDate` como CharField, lo cual no es ideal.
        # Si se pasa un `offer_availability_id`, intentamos filtrar por la cadena de texto del horario.
        # Una mejor solución a futuro sería tener una ForeignKey de ClientClasses a OfferAvailability.
        if offer_availability_id:
            try:
                availability = OfferAvailability.objects.get(id=offer_availability_id)
                # Formateamos el tiempo para que coincida con cómo podría estar guardado en el CharField
                schedule_string = availability.time.strftime("%I:%M %p").lower()  # ej: "01:00 pm"
                # Esta línea es frágil. Depende de que el formato en la BD sea consistente.
                client_list_qs = client_list_qs.filter(scheduleOfferDate__icontains=schedule_string)
            except OfferAvailability.DoesNotExist:
                return Response({"error": "El horario con el ID proporcionado no existe."},
                                status=status.HTTP_404_NOT_FOUND)

        # 4. Generar la respuesta según el tipo de reporte

        # Reportes que comparten la misma estructura de respuesta
        if report_type in ['asistencia', 'comparecencia', 'hoja_de_registro']:
            client_serializer = ReportClientSerializer(client_list_qs, many=True)
            offer_serializer = ReportOfferDetailSerializer(offer)

            response_data = {
                "client_list": client_serializer.data,
                "offer_details": offer_serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)

        # Reporte "COMPARECENCIA TODO"
        if report_type == 'comparecencia_todo':
            client_serializer = ReportClientSerializer(client_list_qs, many=True)

            # Obtenemos todos los bookings para esta oferta
            bookings_qs = Booking.objects.filter(offer=offer).select_related('client')
            booking_serializer = ReportBookingSerializer(bookings_qs, many=True)

            response_data = {
                "client_list": client_serializer.data,
                "bookings": booking_serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)

        # Fallback por si se añade un nuevo tipo de reporte y se olvida la lógica
        return Response({"error": "Lógica de reporte no implementada."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)