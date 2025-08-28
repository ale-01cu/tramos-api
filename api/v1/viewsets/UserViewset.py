from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action

from api.models import User
from api.v1.serializers import UserSerializer, ChangePasswordSerializer, UserCreateSerializer, UserUpdateSerializer
from api.v1.pagination import PaginationCursorPagination
from api.v1.permissions.IsAdminPermission import IsAdminPermission


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminPermission]
    pagination_class = PaginationCursorPagination

    def create(self, request, *args, **kwargs):
        # Obtener el serializador de creación
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Encriptar la contraseña antes de guardar
        password = serializer.validated_data.get('password')
        if password:
            serializer.validated_data['password'] = make_password(password)

        # Crear el usuario
        self.perform_create(serializer)

        # No retornar la contraseña en la respuesta
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data
        if 'password' in response_data:
            del response_data['password']

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        # Obtener la instancia del usuario (no usar request.user)
        instance = self.get_object()

        # Pasar la instancia al serializador para actualización parcial
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True  # Importante para PATCH
        )
        serializer.is_valid(raise_exception=True)

        # Guardar los cambios
        serializer.save()

        return Response(serializer.data)


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



