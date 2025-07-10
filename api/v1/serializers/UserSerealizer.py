from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.v1.serializers.SchoolSerializer import SchoolSerializer

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
    school = SchoolSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

class UserCreateSerializer(serializers.ModelSerializer):
    rol = serializers.CharField(read_only=True)
    full_name = serializers.CharField(max_length=100)
    username = serializers.CharField(validators=[
        UniqueValidator(
            queryset=User.objects.all(),
            message="El usuario no puede ser utilizado",
        )]
    )
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'rol', 'full_name', 'username', 'password',
                  'email', 'school', 'is_superuser', 'is_staff',
                  'is_active')


class UserUpdateSerializer(serializers.ModelSerializer):
    rol = serializers.CharField(read_only=True)
    full_name = serializers.CharField(max_length=100)
    username = serializers.CharField(validators=[
        UniqueValidator(
            queryset=User.objects.all(),
            message="El usuario no puede ser utilizado",
        )]
    )
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'rol', 'full_name', 'username',
                  'email', 'school', 'is_superuser', 'is_staff',
                  'is_active')




