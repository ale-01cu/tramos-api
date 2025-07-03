from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from api.models import Course
from api.v1.permissions import CoursePermission
from api.v1.serializers import CourseSerializer


class CourseViewset(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CoursePermission]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['name']

    def get_queryset(self):
        queryset = self.queryset
        service = self.request.query_params.get('service')
        if not service:
            raise ValidationError('Service is required')
        queryset = queryset.filter(service=service)
        return queryset
