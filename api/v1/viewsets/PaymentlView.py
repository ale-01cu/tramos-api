# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.v1.serializers import PaymentSerializer, TransfermovilCallbackSerializer
from api.transfermovil_payment import register  # Asumiendo que tu función está en utils.py
from django.conf import settings
from datetime import datetime
import hashlib, base64, requests, json
from api.models.TransfermovilNotification import TransfermovilNotification

class PaymentAPIView(APIView):
    serializer_class = PaymentSerializer

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extraer datos validados
        amount = serializer.validated_data['amount']
        phone_number = serializer.validated_data['phone_number']
        external_id = serializer.validated_data['external_id']

        # Llamar a tu función register
        success, qr_data, order_data = register(amount, phone_number, external_id)

        if success:
            TransfermovilNotification.objects.create(
                source=settings.TM_SOURCE,
                bank_id=settings.TM_USERNAME,
                tm_id=order_data,
                phone=phone_number,
                msg="Pago Realizado",
                external_id=external_id,
                status=3,
                bank=None,
                paid=amount,
                is_pending=True
            )

            response_data = {
                'status': 'success',
                'qr_data': qr_data,
                'order_id': order_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'status': 'error',
                'message': 'Payment processing failed',
                'details': order_data  # Aquí order_data contiene la respuesta del error
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)



class PaymentNotificationAPIView(APIView):
    def post(self, request):
        serializer = TransfermovilCallbackSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'Datos de solicitud incorrectos'}, status=status.HTTP_400_BAD_REQUEST)

        external_id = serializer.validated_data['ExternalId']
        source = settings.TM_SOURCE  # Configurar en settings.py
        usuario = settings.TM_USERNAME
        semilla = settings.TM_SEED

        # Obtener fecha actual (hora de Cuba)
        now = datetime.now()
        dia = now.day
        mes = now.month
        year = now.year

        # Generar contraseña
        password_str = f"{usuario}{dia}{mes}{year}{semilla}{source}"
        password_hash = hashlib.sha512(password_str.encode()).digest()
        password = base64.b64encode(password_hash).decode()

        # URL de consulta
        url = f"{settings.TM_CONNECTION}getStatusOrder/{external_id}/{source}"

        # Headers
        headers = {
            'Content-Type': 'application/json',
            'username': usuario,
            'source': source,
            'password': password
        }

        try:
            # Realizar la petición GET (verificar=False solo para desarrollo)
            response = requests.get(
                url,
                headers=headers,
                verify=False  # En producción debería ser True con certificados adecuados
            )

            if response.status_code != 200:
                return Response(
                    {'error': 'Error al realizar la solicitud GET', 'details': response.text},
                    status=status.HTTP_502_BAD_GATEWAY
                )

            data = response.json()
            status_order = data.get('GetStatusOrderResult', {}).get('Status')

            if status_order == 3:  # Pago exitoso
                # Aquí va tu lógica para actualizar la base de datos
                try:
                    # Ejemplo: actualizar orden en tu sistema
                    # order = Order.objects.get(external_id=external_id)
                    # order.status = 'completed'
                    # order.save()
                    updated = True  # Cambiar por tu lógica real

                    if not updated:
                        return Response(
                            {'error': 'Error al actualizar la orden en la base de datos'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )

                    return Response({
                        "Success": True,
                        "Resultmsg": "Mensaje ok",
                        "Status": 1
                    })

                except Exception as db_error:
                    return Response(
                        {'error': 'Error en base de datos', 'details': str(db_error)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            else:
                return Response({
                    "Success": False,
                    "Resultmsg": f"Estado de orden no exitoso: {status_order}",
                    "Status": status_order
                })

        except requests.exceptions.RequestException as e:
            return Response(
                {'error': 'Error de conexión con Transfermóvil', 'details': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except json.JSONDecodeError:
            return Response(
                {'error': 'Error al decodificar la respuesta JSON'},
                status=status.HTTP_502_BAD_GATEWAY
            )
