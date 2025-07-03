from datetime import timedelta

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.models import Offer, OfferAvailability, Course
from api.v1.permissions import OfferPermission
from api.v1.serializers import OfferSerializer, OfferCreateSerializer


class OfferViewset(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = (OfferPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('classroom', 'description', 'course')

    def get_queryset(self):
        queryset = self.queryset
        course = self.request.query_params.get('course', None)
        if not course:
            raise ValidationError('Course is required')
        queryset = queryset.filter(course=course)
        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = OfferCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        start_course = request.query_params.get('date_start_course')
        end_course = request.query_params.get('date_end_course')
        start_offer = request.query_params.get('date_start_offer')
        end_offer = request.query_params.get('date_end_offer')
        if start_course < end_offer + timedelta(days=3):
            raise ValidationError({'fechas inválidas': ["La fecha de fin de la oferta, debe ser al menos 3 días mayor "
                                                        "que la del inicio del curso"]})

        course = request.query_params.get('course')
        classroom = request.query_params.get('classroom')
        company = request.query_params.get('company', None)
        description = request.query_params.get('description')

        price = Course.objects.get(id=course).priceToPay

        try:
            offer = Offer.objects.create(
                course=course,
                description=description,
                priceToPay=price,
                company=company,
                classroom=classroom,
                date_start_offer=start_offer,
                date_end_offer=end_offer,
                date_start_course=start_course,
                date_end_course=end_course
            )
        except:
            return Response({'detail': 'Error al crear la oferta'}, status=status.HTTP_400_BAD_REQUEST)

        availability = request.query_params.get('availability')
        for value in availability:
            OfferAvailability.objects.create(
                offer=offer,
                time=value['time'],
                availability=value['availability'],
                group_code=value['group_code'],
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



