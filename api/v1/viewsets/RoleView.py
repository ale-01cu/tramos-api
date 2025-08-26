from rest_framework.views import APIView
from rest_framework.response import Response
from api.v1.serializers import RoleResponseSerializer
from api.models.User import ROLE_CHOICES
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RoleListApiView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Lista de roles",
                examples={
                    "application/json": {
                        "data": [
                            {"value": "admin", "label": "Administrator"},
                            {"value": "user", "label": "Regular User"},
                            {"value": "moderator", "label": "Moderator"}
                        ]
                    }
                },
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'value': openapi.Schema(type=openapi.TYPE_STRING),
                                    'label': openapi.Schema(type=openapi.TYPE_STRING),
                                },
                                required=['value', 'label']
                            )
                        )
                    },
                    required=['data']
                )
            )
        }
    )
    def get(self, request):
        roles = [
            {'value': value, 'label': label}
            for value, label in ROLE_CHOICES
        ]
        response = {
            'data': roles
        }
        return Response(response)
