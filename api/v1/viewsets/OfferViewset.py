from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, permissions, generics
from rest_framework.response import Response

from api.models import Offer, OfferAvailability, Course, Classroom, Company
from api.v1.permissions import OfferPermission
from api.v1.serializers import OfferSerializer, OfferCreateSerializer


class OfferViewset(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    # serializer_class = OfferSerializer
    permission_classes = (permissions.IsAuthenticated, OfferPermission)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('classroom', 'description', 'course')

    def get_serializer_class(self):
        """
        Determina qué serializador usar basado en la acción.
        """
        # self.action contendrá 'list', 'create', 'retrieve', 'update', 'partial_update'
        if self.action in ['create', 'update', 'partial_update']:
            return OfferCreateSerializer  # Usa este para escribir datos

        # Para cualquier otra acción ('list', 'retrieve', etc.), usa el serializador por defecto.
        return OfferSerializer  # Usa este para leer datos


    # def get_queryset(self):
    #     queryset = self.queryset
    #     course = self.request.query_params.get('course', None)
    #     if not course:
    #         raise ValidationError('Course is required')
    #     queryset = queryset.filter(course=course)
    #     return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = OfferCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        start_course = request.data.get('date_start_course')
        end_course = request.data.get('date_end_course')
        start_offer = request.data.get('date_start_offer')
        end_offer = request.data.get('date_end_offer')
        # if end_offer - start_course > timedelta(days=3):
        #     raise ValidationError({'fechas inválidas': ["La fecha de fin de la oferta, debe ser al menos 3 días mayor "
        #                                                 "que la del inicio del curso"]})

        course = request.data.get('course')
        classroom = request.data.get('classroom')
        company = request.data.get('company', None)
        description = request.data.get('description')

        course = Course.objects.get(id=course)
        classroom = Classroom.objects.get(id=classroom)
        company = Company.objects.get(id=company)

        try:
            offer = Offer.objects.create(
                course=course,
                description=description,
                company=company,
                classroom=classroom,
                date_start_offer=start_offer,
                date_end_offer=end_offer,
                date_start_course=start_course,
                date_end_course=end_course
            )
        except Exception as e:
            print(e)
            return Response({'detail': 'Error al crear la oferta'}, status=status.HTTP_400_BAD_REQUEST)

        availability = request.data.get('availability')
        OfferAvailability.objects.create(
            offer=offer,
            time=availability['time'],
            availability=availability['availability'],
            group_code=availability['group_code'],
        )
        return Response(OfferSerializer(offer, context={'request': request}).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
            Use this API endpoint to remove Screenshot.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'offer deleted'})

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

@extend_schema(
    # Añadimos la descripción del parámetro que queremos documentar
    parameters=[
        OpenApiParameter(
            name='school_id',
            description='Filtrar ofertas por el ID de la escuela a la que pertenecen.',
            required=False,
            type=OpenApiTypes.INT # O simplemente type=int
        ),
    ]
)
class OfferListView(generics.ListAPIView):
    """
    Vista para listar ofertas.
    Permite filtrar por escuela a través de un query param: /api/ofertas/?school_id=ID_DE_LA_ESCUELA
    """
    serializer_class = OfferSerializer

    def get_queryset(self):
        """
        Sobrescribimos este método para filtrar el queryset base.
        """
        # El queryset base son todas las ofertas.
        queryset = Offer.objects.all()

        # Obtenemos el 'school_id' de los parámetros de la URL.
        school_id = self.request.query_params.get('school_id', None)

        # Si se proporcionó un school_id, filtramos el queryset.
        if school_id is not None:
            # ¡Aquí está la magia!
            # Usamos `distinct()` para evitar resultados duplicados si las relaciones
            # fueran más complejas (es una buena práctica).
            queryset = queryset.filter(classroom__school__id=school_id).distinct()

        return queryset