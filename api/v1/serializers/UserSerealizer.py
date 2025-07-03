from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.models import User


class UserSerializer(serializers.ModelSerializer):
    rol = serializers.CharField(read_only=True)
    full_name = serializers.CharField(max_length=100)
    username = serializers.CharField(validators=[
        UniqueValidator(
            queryset=User.objects.all(),
            message="El usuario no puede ser utilizado",
        )]
    )

    class Meta:
        model = User
        fields = '__all__'

