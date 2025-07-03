from rest_framework import serializers

from api.v1.serializers import CourseSerializer, ClassroomSerializer, CompanySerializer, OfferAvailabilitySerializer


class OfferCreateSerializer(serializers.Serializer):
    course = CourseSerializer()
    classroom = ClassroomSerializer()
    company = CompanySerializer(required=False)
    description = serializers.CharField()
    availability = serializers.SerializerMethodField()
    date_start_course = serializers.DateTimeField()
    date_end_course = serializers.DateTimeField()
    date_start_offer = serializers.DateTimeField()
    date_end_offer = serializers.DateTimeField()

    @staticmethod
    def get_availability(obj):
        availability = obj.offer_availability.all()
        return OfferAvailabilitySerializer(availability, many=True).data

    # def create(self, validated_data):

