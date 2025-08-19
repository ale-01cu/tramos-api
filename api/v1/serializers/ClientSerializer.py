from rest_framework import serializers

from api.models import Client


class ClientSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    ci = serializers.CharField()
    sex = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'last_name', 'phone_number', 'email', 'sex', 'ci', 'code', 'created_at']
        read_only_fields = ['created_at']


class ClientRelatedField(serializers.RelatedField):
    """
    Un campo de serializador personalizado para representar al cliente.
    Puede aceptar un ID (para un cliente existente) o un diccionario (para crear un nuevo cliente).
    """

    def to_internal_value(self, data):
        # Si 'data' es un entero, asumimos que es el ID de un cliente existente.
        if isinstance(data, int):
            try:
                return Client.objects.get(pk=data)
            except Client.DoesNotExist:
                raise serializers.ValidationError("El cliente con el ID especificado no existe.")

        # Si 'data' es un diccionario, lo validamos para crear un nuevo cliente.
        if isinstance(data, dict):
            # Usamos el ClientSerializer para validar los datos del nuevo cliente.
            serializer = ClientSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            # No creamos el cliente aquí, solo devolvemos los datos validados.
            # La creación se manejará en el método `create` del serializador principal.
            return serializer.validated_data

        raise serializers.ValidationError(
            "El campo 'client' debe ser un ID de cliente (entero) o un objeto con los datos del cliente.")

    def to_representation(self, value):
        # Cuando se serializa una reserva para una respuesta, mostramos los datos completos del cliente.
        # 'value' aquí es una instancia del modelo Client.
        return ClientSerializer(value).data


class ChangeCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)