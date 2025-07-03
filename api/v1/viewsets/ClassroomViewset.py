from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import ValidationError

from api.models import Classroom
from api.v1.serializers import ClassroomSerializer


class ClassroomViewset(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'school']

    def get_queryset(self):
        queryset = self.queryset
        school = self.request.query_params.get('school')
        if not school:
            raise ValidationError('School is required')
        queryset = queryset.filter(school=school)
        return queryset


