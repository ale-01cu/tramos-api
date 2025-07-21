from rest_framework import serializers

from api.models import Offer, OfferAvailability
from api.v1.serializers import ClassroomSerializer, CourseSerializer, CompanySerializer

class OfferSerializer(serializers.ModelSerializer):
    classroom = ClassroomSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    # classroom = serializers.CharField(source='classroom.name')
    # date_start_course = serializers.DateField()
    # availability = serializers.SerializerMethodField()
    # company = serializers.CharField(source='company.name', allow_blank=True, allow_null=True)
    # description = serializers.CharField(max_length=250)

    @staticmethod
    def get_availability(offer):
        try:
            availability = OfferAvailability.objects.filter(offer=offer)
            total = 0
            for availability in availability:
                total += availability.availability
            return total
        except Exception as e:
            raise e

    class Meta:
        model = Offer
        fields = '__all__'
