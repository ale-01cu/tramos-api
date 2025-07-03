from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class TokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user'] = dict(
            username=user.username,
            full_name=user.full_name,
            rol=user.rol,
            is_active=user.is_active,
        )
        # terminar de poner los datos q mando del usuario q se autentica
        return token
