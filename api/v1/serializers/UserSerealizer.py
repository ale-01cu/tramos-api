from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.v1.serializers.SchoolSerializer import SchoolSerializer

from api.models import User
from api.models.User import ROLE_CHOICES


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
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
        fields = (
            'id', 'role', 'is_active', 'first_name', 'last_name',
            'full_name', 'username', 'school',
            'email', 'created_at'
        )

class UserCreateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES)
    full_name = serializers.CharField(max_length=100)
    username = serializers.CharField(validators=[
        UniqueValidator(
            queryset=User.objects.all(),
            message="El usuario no puede ser utilizado",
        )]
    )
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'role', 'full_name', 'username', 'password',
                  'email', 'school', 'is_active', 'created_at')
        read_only_fields = ['created_at']


class UserUpdateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=False)
    full_name = serializers.CharField(max_length=100, required=False)
    username = serializers.CharField(validators=[
        UniqueValidator(
            queryset=User.objects.all(),
            message="El usuario no puede ser utilizado",
        )], required=False
    )
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'role', 'full_name', 'username',
                  'email', 'school', 'is_active')




