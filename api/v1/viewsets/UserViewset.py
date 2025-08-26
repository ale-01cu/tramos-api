from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action

from api.models import User
from api.v1.serializers import UserSerializer, ChangePasswordSerializer, UserCreateSerializer, UserUpdateSerializer
from api.v1.pagination import PaginationCursorPagination


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PaginationCursorPagination

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['full_name']:
            new_name = serializer.validated_data['full_name']
            user.full_name = new_name
            user.save()
        if serializer.validated_data['is_active']:
            user.is_active = not user.is_active
            user.save()

    @action(detail=True, methods=['PATCH'], serializer_class=ChangePasswordSerializer)
    def change_password(self, request, pk=None):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        password = serializer.validated_data['new_password']
        password = make_password(password)
        user.password = password
        user.save()
        return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        """
        Determina qué serializador usar basado en la acción.
        """
        # self.action contendrá 'list', 'create', 'retrieve', 'update', 'partial_update'
        if self.action in ['create']:
            return UserCreateSerializer  # Usa este para escribir datos

        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer  # Usa este para escribir datos

        # Para cualquier otra acción ('list', 'retrieve', etc.), usa el serializador por defecto.
        return UserSerializer  # Usa este para leer datos



