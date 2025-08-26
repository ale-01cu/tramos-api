from rest_framework import serializers

class RoleResponseSerializer(serializers.Serializer):
    value = serializers.CharField(help_text="Valor interno del rol para almacenar")
    label = serializers.CharField(help_text="Nombre legible para mostrar")