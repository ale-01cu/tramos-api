from rest_framework import serializers
from api.v1.serializers.OfferAvailabilitySerializer import OfferAvailabilityCreateWithOfferSerializer
from datetime import timedelta
from api.models import Offer

# class OfferCreateSerializer(serializers.Serializer):
#     course = CourseSerializer()
#     classroom = ClassroomSerializer()
#     company = CompanySerializer(required=False)
#     description = serializers.CharField()
#     availability = serializers.SerializerMethodField()
#     date_start_course = serializers.DateTimeField()
#     date_end_course = serializers.DateTimeField()
#     date_start_offer = serializers.DateTimeField()
#     date_end_offer = serializers.DateTimeField()
#
#     @staticmethod
#     def get_availability(obj):
#         availability = obj.offer_availability.all()
#         return OfferAvailabilitySerializer(availability, many=True).data


class OfferCreateSerializer(serializers.ModelSerializer):
    availability = OfferAvailabilityCreateWithOfferSerializer()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Offer
        fields = ['course', 'classroom', 'description', 'availability',
                  'date_start_course', 'date_end_course',
                  'date_start_offer', 'date_end_offer', 'company', 'created_at']
        read_only_fields = ['created_at']
        # extra_kwargs = {'price': {'required': True}}

    def validate(self, data):
        """
        Validaciones a nivel de objeto para comparar campos entre sí.
        """
        start_course = data['date_start_course']
        end_offer = data['date_end_offer']

        # DRF ya ha convertido las fechas a objetos datetime, así que la comparación funciona.
        if start_course and end_offer:
            if end_offer - start_course > timedelta(days=3):
                raise serializers.ValidationError({
                    'fechas': "La fecha de fin de la oferta debe ser al menos 3 días posterior al inicio del curso."
                })

        return data

    # def create(self, validated_data):
    #     availability_data = validated_data.pop('availability')
    #     time = availability_data['time']
    #     availability = availability_data['availability']
    #     group_code = availability_data['group_code']
    #
    #     print("antes")
    #     offer = Offer.objects.create(**validated_data)
    #     print("despues")
    #
    #     # Ahora 'correct_time' siempre será del tipo que necesitamos
    #     OfferAvailability.objects.create(
    #         offer=offer,
    #         # time=time,
    #         time=time,
    #         availability=availability,
    #         group_code=group_code
    #     )
    #     print("mucho despues")
    #
    #     return offer
